"""
Smart M3U parsing with full EXTINF metadata extraction.
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional
from .utils import detect_country_from_group


@dataclass
class Stream:
    url: str
    name: str
    tvg_id: str = ""
    tvg_name: str = ""
    tvg_logo: str = ""
    group_title: str = ""
    tvg_language: str = ""
    tvg_country: str = ""
    has_cookies: bool = False
    vlc_opts: list[str] | None = None


class M3UParser:
    """Parser class for M3U playlist content."""

    def parse(self, content: str) -> List[dict]:
        """Parse M3U content and return list of channel dicts for backwards compatibility / tests."""
        streams = parse_m3u(content)
        result = []
        for s in streams:
            group = s.group_title or "Uncategorized"
            group_detected = detect_country_from_group(group)
            result.append({
                "name": s.name,
                "url": s.url,
                "tvg_id": s.tvg_id,
                "tvg_name": s.tvg_name,
                "tvg_logo": s.tvg_logo,
                "group": group_detected,
                "has_cookies": s.has_cookies,
            })
        return result

    def parse_all(self, sources: List[dict]) -> List[dict]:
        """Parse multiple sources list of dicts {'source': url, 'content': text}."""
        all_channels = []
        for s in sources:
            all_channels.extend(self.parse(s.get("content", "")))
        return all_channels


def parse_m3u(content: str) -> List[Stream]:
    """Parse M3U string into Stream objects."""
    streams: List[Stream] = []
    lines = content.splitlines()
    current_stream: Optional[Stream] = None
    vlc_opts: list[str] = []

    extinf_re = re.compile(r"#EXTINF:-1(.*),(.*)")
    prop_re = re.compile(r'([a-zA-Z0-9_-]+)="([^"]*)"')

    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF"):
            match = extinf_re.match(line)
            if match:
                props_str, name = match.groups()
                props = dict(prop_re.findall(props_str))
                current_stream = Stream(
                    url="",
                    name=name.strip(),
                    tvg_id=props.get("tvg-id", ""),
                    tvg_name=props.get("tvg-name", ""),
                    tvg_logo=props.get("tvg-logo", ""),
                    group_title=props.get("group-title", ""),
                    tvg_language=props.get("tvg-language", ""),
                    tvg_country=props.get("tvg-country", ""),
                )
        elif line.startswith("#EXTVLCOPT"):
            vlc_opts.append(line)
        elif line and not line.startswith("#"):
            if current_stream:
                current_stream.url = line
                current_stream.vlc_opts = list(vlc_opts)
                if any("Cookie:" in opt for opt in vlc_opts):
                    current_stream.has_cookies = True
                streams.append(current_stream)
                current_stream = None
                vlc_opts = []

    return streams
