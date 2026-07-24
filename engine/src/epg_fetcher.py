"""
EPG Fetcher — Fetch and parse Electronic Program Guide (XMLTV) data.
"""

import asyncio
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Dict, List, Optional
import aiohttp
from .utils import logger


@dataclass
class EPGProgram:
    channel_id: str
    title: str
    start: str
    stop: str
    description: str = ""
    category: str = ""


class EPGFetcher:
    """Class wrapper for fetching and parsing XMLTV EPG data."""

    def parse_epg_programs(self, xml_content: str) -> List[dict]:
        """Parse raw XMLTV string into list of dicts for test compatibility."""
        programs = []
        try:
            root = ET.fromstring(xml_content)
            for programme in root.findall(".//programme"):
                channel_id = programme.get("channel", "")
                start = programme.get("start", "")
                stop = programme.get("stop", "")

                title_elem = programme.find("title")
                title = title_elem.text if title_elem is not None and title_elem.text else ""

                desc_elem = programme.find("desc")
                desc = desc_elem.text if desc_elem is not None and desc_elem.text else ""

                category_elem = programme.find("category")
                category = category_elem.text if category_elem is not None and category_elem.text else ""

                programs.append({
                    "channel_id": channel_id,
                    "title": title,
                    "start": start,
                    "stop": stop,
                    "desc": desc,
                    "category": category,
                })
        except Exception as e:
            logger.error(f"Error parsing EPG XML: {e}")
        return programs


async def fetch_epg(url: str, timeout: int = 60) -> List[EPGProgram]:
    programs: List[EPGProgram] = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout), ssl=False) as resp:
                resp.raise_for_status()
                content = await resp.text(errors="replace")

        fetcher = EPGFetcher()
        parsed = fetcher.parse_epg_programs(content)
        for p in parsed:
            programs.append(EPGProgram(
                channel_id=p["channel_id"],
                title=p["title"],
                start=p["start"],
                stop=p["stop"],
                description=p["desc"],
                category=p["category"],
            ))
    except Exception as exc:
        logger.warning(f"Failed to fetch EPG from {url}: {exc}")

    return programs
