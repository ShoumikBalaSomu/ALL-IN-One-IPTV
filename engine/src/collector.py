import asyncio
from typing import List
from .utils import get_logger

logger = get_logger(__name__)

class Collector:
    def __init__(self, sources: List[str]):
        self.sources = sources

    async def fetch_source(self, url: str) -> str:
        # Mock fetching
        await asyncio.sleep(0.01)
        if url.startswith("http"):
            return "#EXTM3U\n#EXTINF:-1,Test Channel\nhttp://test.com/stream.m3u8"
        return ""

    async def collect(self) -> str:
        tasks = [self.fetch_source(src) for src in self.sources]
        results = await asyncio.gather(*tasks)
        return "\n".join(results)
