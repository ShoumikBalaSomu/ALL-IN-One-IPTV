"""
Playlist Collector — Fetch M3U playlists from URLs and local files.
"""

import asyncio
import aiohttp
import os
import glob
import base64
from typing import Optional

from .utils import setup_logging, url_hash

logger = setup_logging("engine.collector")

# Default playlist sources
DEFAULT_PLAYLISTS = [
    "https://raw.githubusercontent.com/sm-monirulislam/SM-Live-TV/refs/heads/main/Combined_Live_TV.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/SM-Movie-Hup-Auto-Update/refs/heads/main/Movie_Combined.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/AynaOTT-auto-update-playlist/refs/heads/main/AynaOTT.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/Toffee-Auto-Update-Playlist/refs/heads/main/toffee_playlist.m3u",
    "https://private-zone-by-xfireflix.pages.dev/BDIX1.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/BDxTV/refs/heads/main/playlist_s.m3u",
    "https://movie-playlist-byxfireflix.pages.dev/movie-playlist.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/Movie-Playlist-Auto-update/refs/heads/main/Mix_Movies.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/main/playlist.m3u",
    "https://raw.githubusercontent.com/ashik4u/mrgify-clean/refs/heads/main/playlist.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/Toffee-playlist/refs/heads/main/ott_navigator.m3u",
    "https://raw.githubusercontent.com/Mrbotrx/bdxi_tv/main/kbtvpro.m3u8",
    "https://raw.githubusercontent.com/johirxofficial/aynaott-auto-update-playlist/refs/heads/main/AynaOTT.m3u",
    "https://raw.githubusercontent.com/johirxofficial/Toffee-Auto-Playlist/refs/heads/main/toffee_playlist.m3u",
    "https://raw.githubusercontent.com/tahsinulmohsin/jagobd-m3u8-scraper/master/playlist.m3u8",
    "https://raw.githubusercontent.com/ashik4u/iptv-m3u-bot/refs/heads/main/output/all.m3u",
    "https://raw.githubusercontent.com/opensourceflix/OpenSourceFlix/refs/heads/main/iptv.m3u8",
    "https://raw.githubusercontent.com/etcvai/ExtenderMax/refs/heads/main/iptv.m3u8",
    "https://raw.githubusercontent.com/opensourceflix/OpenSourceFlix/main/papaos.m3u8",
    "https://go.skym3u.top/fyeo.m3u",
    "https://raw.githubusercontent.com/sanjoykb/-KB-TV-Playlist/refs/heads/main/Github%20Auto%20Update%20Channel.m3u",
    "https://raw.githubusercontent.com/alberttartas/Pirataflix/refs/heads/main/input_auto/TV/iptv_org_br.m3u",
    "https://raw.githubusercontent.com/alberttartas/Pirataflix/refs/heads/main/iptv_playlists/vod_grouped.m3u",
    "http://202.70.146.135:8000/playlist.m3u",
    "https://iptvidn-playlist.vercel.app/playlist.m3u8",
    "https://raw.githubusercontent.com/abusaeeidx/IPTV-Scraper-Zilla/main/combined-playlist.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/Yupptv-Playlist/refs/heads/main/playlist.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/Yupptv-Playlist/refs/heads/main/playlist_v2.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/CricHd-playlists-Auto-Update-permanent/refs/heads/main/ALL.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/CricHD-Scraper-V2/main/playlist.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/IP-Stream/refs/heads/main/playlist.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/FanCode-Auto-Update-Playlist/refs/heads/main/fancode_bd.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/FanCode-Auto-Update-Playlist/refs/heads/main/fancode_in.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/Tapmad_Auto_Update_Playlist/refs/heads/main/Tapmad_sm.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/CricHD-Auto-Update-Playlist/refs/heads/main/crichd.m3u",
    "https://raw.githubusercontent.com/Love4vn/Love4xt/refs/heads/1/output.m3u",
    "https://raw.githubusercontent.com/Love4vn/Love4xt/refs/heads/1/output_clean.m3u",
    "https://raw.githubusercontent.com/Love4vn/Match_Stream/refs/heads/1/Football_match_live.m3u",
    "https://raw.githubusercontent.com/Love4vn/Match_Stream/refs/heads/1/Mac_playlist.m3u",
    "https://raw.githubusercontent.com/Love4vn/Match_Stream/refs/heads/1/live_schedule_Optimize.m3u",
    "https://raw.githubusercontent.com/Love4vn/Test/refs/heads/main/IPTV.m3u",
    "https://raw.githubusercontent.com/Love4vn/Stalker2M3U-public/refs/heads/main/Mac_playlist.m3u",
    "https://raw.githubusercontent.com/Love4vn/Stalker2M3U-public/refs/heads/main/Football_match_live.m3u",
    "https://raw.githubusercontent.com/Love4vn/Stalker2M3U-public/refs/heads/main/live_schedule_Optimize.m3u",
    "https://raw.githubusercontent.com/Mrbotrx/Tvbox_KB/main/kb_tv.m3u",
    "https://raw.githubusercontent.com/Mrbotrx/All-FREE-TV/main/combined_playlist.m3u",
    "https://raw.githubusercontent.com/johirxofficial/otv-auto-updated-playlist/main/otv.m3u",
    "https://raw.githubusercontent.com/imShakil/tvlink/refs/heads/main/all.m3u",
    "https://link.dekhoprime.live/m3u/bd/1782385148-ant-ferret-dingo.m3u",
    "https://link.dekhoprime.live/m3u/world/1782385148-moose-wolf-goose.m3u",
    "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/jtv.m3u",
    "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/jstar.m3u",
    "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/jcinema.m3u",
    "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/amzusa.m3u",
    "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/dishtv.m3u",
    "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/lgtv.m3u",
    "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/suntv.m3u",
    "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/z5.m3u",
    "https://raw.githubusercontent.com/judy-gotv/iptv/refs/heads/main/combined-playlist.m3u",
    "https://la.drmlive.net/tp/playlist",
    "https://raw.githubusercontent.com/bugsfreeweb/LiveTVCollector/refs/heads/main/LiveTV/Bangladesh/LiveTV.m3u",
    "https://raw.githubusercontent.com/zilong7728/Collect-IPTV/refs/heads/main/best_sorted.m3u",
    "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8",
    "https://iptv-org.github.io/iptv/index.m3u",
    "https://raw.githubusercontent.com/ewchew/sports/main/liveeventsfilter.m3u8",
    "https://www.apsattv.com/localnow.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/tcl-playlist-generator/refs/heads/main/tcl.m3u8",
    "https://raw.githubusercontent.com/BuddyChewChew/lg-playlist-generator/refs/heads/main/lg_channels_us.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/xumo-playlist-generator/refs/heads/main/playlists/xumo_playlist.m3u",
    "https://raw.githubusercontent.com/Alplox/json-teles/refs/heads/main/channels.m3u",
    "https://romaxa55.github.io/world_ip_tv/output/index.m3u",
    "https://raw.githubusercontent.com/joaquinito2036-rgb/iptvfast/refs/heads/main/output/all.m3u",
]


class PlaylistCollector:
    """Collect M3U playlists from remote URLs and local files."""

    def __init__(
        self,
        playlist_urls: list[str] | None = None,
        decrypt_key: str | None = None,
        timeout: int = 15,
    ):
        self.playlist_urls = playlist_urls or DEFAULT_PLAYLISTS
        self.decrypt_key = decrypt_key
        self.timeout = timeout

    async def fetch_url(self, session: aiohttp.ClientSession, url: str) -> dict | None:
        """Fetch a single playlist URL."""
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=self.timeout)) as resp:
                if resp.status == 200:
                    content = await resp.text(encoding='utf-8', errors='ignore')
                    logger.debug(f"Fetched {url} ({len(content)} bytes) [{url_hash(url)}]")
                    return {"source": url, "content": content, "type": "remote"}
                else:
                    logger.warning(f"HTTP {resp.status} for {url}")
        except asyncio.TimeoutError:
            logger.warning(f"Timeout fetching {url}")
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
        return None

    def read_local_file(self, filepath: str) -> dict | None:
        """Read a local M3U/M3U8 file."""
        try:
            # Check if it's an encrypted file
            if filepath.endswith('.enc') and self.decrypt_key:
                return self._decrypt_file(filepath)

            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            logger.debug(f"Read local file {filepath} ({len(content)} bytes)")
            return {"source": filepath, "content": content, "type": "local"}
        except Exception as e:
            logger.error(f"Error reading {filepath}: {e}")
            return None

    def _decrypt_file(self, filepath: str) -> dict | None:
        """Decrypt an AES-256-GCM encrypted playlist file."""
        try:
            from Crypto.Cipher import AES

            key = bytes.fromhex(self.decrypt_key)
            if len(key) != 32:
                logger.error("Decrypt key must be 32 bytes (64 hex chars)")
                return None

            with open(filepath, 'rb') as f:
                iv = f.read(12)
                tag = f.read(16)
                ciphertext = f.read()

            cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)

            logger.debug(f"Decrypted {filepath} ({len(plaintext)} bytes)")
            return {
                "source": filepath,
                "content": plaintext.decode('utf-8', errors='ignore'),
                "type": "local_encrypted",
            }
        except ImportError:
            logger.error("pycryptodome not installed. Run: pip install pycryptodome")
            return None
        except Exception as e:
            logger.error(f"Decryption failed for {filepath}: {e}")
            return None

    async def collect(self, input_dir: str = "input") -> list[dict]:
        """Collect all playlists from remote URLs and local files."""
        results = []

        # Fetch remote playlists concurrently
        logger.info(f"Fetching {len(self.playlist_urls)} remote playlists...")
        connector = aiohttp.TCPConnector(limit=50)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [self.fetch_url(session, url) for url in self.playlist_urls]
            remote_results = await asyncio.gather(*tasks)

        for result in remote_results:
            if result and result.get("content"):
                results.append(result)

        logger.info(f"Successfully fetched {len(results)} remote playlists")

        # Read local playlists
        local_patterns = [
            os.path.join(input_dir, "*.m3u"),
            os.path.join(input_dir, "*.m3u8"),
            os.path.join(input_dir, "*.enc"),
        ]

        local_files = []
        for pattern in local_patterns:
            local_files.extend(glob.glob(pattern))

        if local_files:
            logger.info(f"Found {len(local_files)} local playlist files")
            for filepath in sorted(local_files):
                result = self.read_local_file(filepath)
                if result and result.get("content"):
                    results.append(result)

        return results