"""
EPG (Electronic Program Guide) Fetcher and Aggregator.
Fetches XMLTV guides and merges program schedules for channels.
"""

import gzip
import io
import xml.etree.ElementTree as ET
import aiohttp
import asyncio
from .utils import setup_logging

logger = setup_logging("engine.epg_fetcher")

PUBLIC_EPG_SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/epg/master/providers/example.com.xml",
]

class EPGFetcher:
    """Fetches and parses XMLTV EPG data."""

    def __init__(self, sources=None):
        self.sources = sources or PUBLIC_EPG_SOURCES

    async def fetch_epg_xml(self, session: aiohttp.ClientSession, url: str) -> str | None:
        """Fetch raw XML or GZipped XMLTV content."""
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                if resp.status == 200:
                    content = await resp.read()
                    if url.endswith(".gz") or content[:2] == b'\x1f\x8b':
                        with gzip.GzipFile(fileobj=io.BytesIO(content)) as gz:
                            return gz.read().decode('utf-8', errors='ignore')
                    return content.decode('utf-8', errors='ignore')
        except Exception as e:
            logger.debug(f"Failed to fetch EPG from {url}: {e}")
        return None

    def parse_epg_programs(self, xml_content: str) -> list[dict]:
        """Parse XMLTV channel and programme elements."""
        programs = []
        if not xml_content:
            return programs

        try:
            root = ET.fromstring(xml_content)
            for prog in root.findall('programme'):
                channel_id = prog.get('channel', '')
                start = prog.get('start', '')
                stop = prog.get('stop', '')
                title_elem = prog.find('title')
                desc_elem = prog.find('desc')

                title = title_elem.text if title_elem is not None else 'No Title'
                desc = desc_elem.text if desc_elem is not None else ''

                programs.append({
                    'channel_id': channel_id,
                    'start': start,
                    'stop': stop,
                    'title': title,
                    'desc': desc
                })
        except Exception as e:
            logger.debug(f"Error parsing EPG XML: {e}")

        return programs

    async def fetch_and_aggregate(self) -> list[dict]:
        """Fetch all configured EPG sources and return aggregated program list."""
        logger.info(f"Fetching EPG data from {len(self.sources)} sources...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        all_programs = []
        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = [self.fetch_epg_xml(session, url) for url in self.sources]
            results = await asyncio.gather(*tasks)
            for xml_content in results:
                if xml_content:
                    parsed = self.parse_epg_programs(xml_content)
                    all_programs.extend(parsed)

        logger.info(f"Aggregated {len(all_programs)} EPG program entries.")
        return all_programs
