import asyncio
import aiohttp
from typing import List
from .utils import get_logger

logger = get_logger(__name__)

DEFAULT_SOURCES = [
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
    "https://iptv-org.github.io/iptv/index.m3u",
    "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8"
]

class Collector:
    def __init__(self, sources: List[str] = None):
        self.sources = sources or DEFAULT_SOURCES

    async def fetch_source(self, session: aiohttp.ClientSession, url: str) -> str:
        try:
            timeout = aiohttp.ClientTimeout(total=15)
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) IPTV-Engine/2.1.0"}
            async with session.get(url, timeout=timeout, headers=headers, ssl=False) as resp:
                if resp.status == 200:
                    text = await resp.text(errors="replace")
                    logger.info(f"Fetched {len(text)} bytes from {url}")
                    return text
                else:
                    logger.warning(f"HTTP {resp.status} fetching {url}")
                    return ""
        except Exception as e:
            logger.warning(f"Error fetching {url}: {e}")
            return ""

    async def collect(self) -> str:
        connector = aiohttp.TCPConnector(limit=15, ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [self.fetch_source(session, src) for src in self.sources]
            results = await asyncio.gather(*tasks)
            return "\n".join(res for res in results if res)
