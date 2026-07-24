"""
Xtream Codes API Parser.
Parses Xtream Codes server endpoints and transforms categories and streams to folded M3U structures.
"""

import aiohttp
from .utils import setup_logging

logger = setup_logging("engine.xtream_parser")

class XtreamParser:
    """Parser for Xtream Codes server portals."""

    def __init__(self, host: str, username: str, password: str):
        self.host = host.rstrip('/')
        self.username = username
        self.password = password

    @property
    def base_url(self) -> str:
        return f"{self.host}/player_api.php?username={self.username}&password={self.password}"

    async def fetch_live_categories(self, session: aiohttp.ClientSession) -> list[dict]:
        """Fetch live TV categories."""
        url = f"{self.base_url}&action=get_live_categories"
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    return await resp.json()
        except Exception as e:
            logger.debug(f"Failed to fetch Xtream categories from {self.host}: {e}")
        return []

    async def fetch_live_streams(self, session: aiohttp.ClientSession) -> list[dict]:
        """Fetch live streams list."""
        url = f"{self.base_url}&action=get_live_streams"
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 200:
                    return await resp.json()
        except Exception as e:
            logger.debug(f"Failed to fetch Xtream streams from {self.host}: {e}")
        return []

    def convert_to_m3u_items(self, streams: list[dict], categories: list[dict] | None = None) -> list[dict]:
        """Convert Xtream json stream entries to standard M3U channel items."""
        cat_map = {str(c.get('category_id')): c.get('category_name', 'Xtream') for c in (categories or [])}
        items = []

        for s in streams:
            stream_id = s.get('stream_id')
            name = s.get('name', 'Xtream Stream')
            cat_id = str(s.get('category_id', ''))
            group = cat_map.get(cat_id, 'Xtream Live')
            logo = s.get('stream_icon', '')
            container_ext = s.get('container_extension', 'm3u8')

            stream_url = f"{self.host}/live/{self.username}/{self.password}/{stream_id}.{container_ext}"

            extinf = f'#EXTINF:-1 tvg-id="{s.get("epg_channel_id", "")}" tvg-logo="{logo}" group-title="{group}",{name}'

            items.append({
                'name': name,
                'group': group,
                'logo': logo,
                'extinf': extinf,
                'vlc_opts': [],
                'url': stream_url,
                'has_cookies': False
            })

        return items
