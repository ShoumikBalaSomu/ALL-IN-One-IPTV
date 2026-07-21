"""
Deduplicator — Remove duplicate channel URLs while preserving special channels.
"""

from .utils import setup_logging, url_hash, has_special_headers

logger = setup_logging("engine.deduplicator")


class Deduplicator:
    """Remove duplicate URLs while preserving channels with cookies/tokens."""

    def deduplicate(self, channels: list[dict]) -> list[dict]:
        """Remove exact URL duplicates, keeping channels with special headers."""
        seen_urls: dict[str, dict] = {}
        special_channels: list[dict] = []  # Channels with cookies/tokens — always keep

        for ch in channels:
            url = ch["url"]
            url_h = url_hash(url)
            is_special = ch.get("has_cookies", False)

            if is_special:
                # Always keep channels with cookies/tokens
                special_channels.append(ch)
                continue

            if url_h not in seen_urls:
                seen_urls[url_h] = ch

        # Merge: unique non-special + all special
        result = list(seen_urls.values()) + special_channels

        removed = len(channels) - len(result)
        logger.info(f"Deduplication: {len(channels)} → {len(result)} ({removed} duplicates removed)")

        return result

    def deduplicate_by_name(self, channels: list[dict], keep_first: bool = True) -> list[dict]:
        """Deduplicate by channel name within the same group.

        Useful for when the same channel appears with identical names.
        """
        from collections import defaultdict

        seen: dict[str, dict] = {}
        result = []

        for ch in channels:
            key = f"{ch.get('group', '')}:{ch.get('name', '')}"

            if key not in seen:
                seen[key] = ch
                result.append(ch)
            elif ch.get("has_cookies", False):
                # Keep if this one has special headers
                result.append(ch)

        removed = len(channels) - len(result)
        logger.info(f"Name deduplication: {len(channels)} → {len(result)} ({removed} removed)")

        return result