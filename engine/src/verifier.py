"""
Link Verifier — Check if stream URLs are alive using parallel HTTP requests.

Uses host-level checking: if one URL from a host responds, all URLs from
that host are considered alive. This dramatically speeds up verification
for playlists with thousands of channels sharing the same CDN.
"""

import asyncio
import aiohttp
from urllib.parse import urlparse
from collections import defaultdict

from .utils import setup_logging, url_to_host

logger = setup_logging("engine.verifier")


class LinkVerifier:
    """Verify stream URLs are accessible using parallel host-level checking."""

    def __init__(self, concurrency: int = 100, timeout: int = 5):
        self.concurrency = concurrency
        self.timeout = timeout

    async def check_host(self, session: aiohttp.ClientSession, url: str) -> bool:
        """Check if a single URL responds with a successful status."""
        try:
            # Use HEAD request first (faster, less bandwidth)
            async with session.head(
                url,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                allow_redirects=True,
            ) as resp:
                if resp.status < 400:
                    return True

            # If HEAD fails, try GET with low timeout (some servers block HEAD)
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                allow_redirects=True,
            ) as resp:
                return resp.status < 400

        except asyncio.TimeoutError:
            return False
        except Exception:
            return False

    async def verify(self, channels: list[dict]) -> list[dict]:
        """Verify all channels using host-level health checking.

        Strategy:
        1. Map each channel to its host
        2. Check one representative URL per host
        3. If host is alive, all channels from that host are alive
        4. For channels with cookies/special headers, always include them
        """
        # Build host map
        host_map: dict[str, list[dict]] = defaultdict(list)
        standalone: list[dict] = []  # Channels with special headers — always keep

        for ch in channels:
            url = ch["url"]
            if ch.get("has_cookies", False):
                standalone.append(ch)
                continue

            # For folded channels, check the primary URL
            host = url_to_host(url)
            host_map[host].append(ch)

        logger.info(f"Checking {len(host_map)} unique hosts...")

        # Check hosts in parallel
        alive_hosts: set[str] = set()
        connector = aiohttp.TCPConnector(limit=self.concurrency)

        async with aiohttp.ClientSession(connector=connector) as session:
            semaphore = asyncio.Semaphore(self.concurrency)

            async def check_host_with_sem(host: str, sample_url: str):
                async with semaphore:
                    is_alive = await self.check_host(session, sample_url)
                    if is_alive:
                        alive_hosts.add(host)
                    else:
                        logger.debug(f"Dead host: {host}")

            tasks = [
                check_host_with_sem(host, host_map[host][0]["url"])
                for host in host_map
            ]

            # Process in batches with progress reporting
            for i, task in enumerate(asyncio.as_completed(tasks)):
                await task
                if (i + 1) % 50 == 0:
                    logger.info(f"Checked {i + 1}/{len(tasks)} hosts ({len(alive_hosts)} alive)")

        # Filter channels: keep if host is alive OR channel has special headers
        verified = []
        for ch in channels:
            if ch.get("has_cookies", False):
                verified.append(ch)
                continue

            host = url_to_host(ch["url"])
            if host in alive_hosts:
                verified.append(ch)

        logger.info(
            f"Verification complete: {len(verified)}/{len(channels)} channels verified "
            f"({len(alive_hosts)}/{len(host_map)} hosts alive)"
        )

        return verified

    async def verify_individual(self, channels: list[dict]) -> list[dict]:
        """Verify each URL individually (slower but more accurate).

        Useful for small playlists or when you need per-URL accuracy.
        """
        verified = []
        connector = aiohttp.TCPConnector(limit=self.concurrency)

        async with aiohttp.ClientSession(connector=connector) as session:
            semaphore = asyncio.Semaphore(self.concurrency)

            async def check_channel(ch: dict):
                async with semaphore:
                    url = ch["url"]
                    is_alive = await self.check_host(session, url)
                    return ch, is_alive

            tasks = [check_channel(ch) for ch in channels]
            for i, task in enumerate(asyncio.as_completed(tasks)):
                ch, is_alive = await task
                if is_alive:
                    verified.append(ch)
                if (i + 1) % 500 == 0:
                    logger.info(f"Checked {i + 1}/{len(channels)} URLs")

        logger.info(f"Individual verification: {len(verified)}/{len(channels)} alive")
        return verified