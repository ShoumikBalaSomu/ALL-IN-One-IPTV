"""
Folder — Output formatting utilities for M3U and JSON exports.
"""

import json
from typing import List
from dataclasses import asdict

from .parser import Stream


def to_m3u(streams: List[Stream]) -> str:
    """
    Convert a list of streams to M3U format string.

    Args:
        streams: List of Stream objects.

    Returns:
        M3U-formatted string.
    """
    lines = ["#EXTM3U", ""]

    for stream in streams:
        attrs = []
        if stream.tvg_id:
            attrs.append(f'tvg-id="{stream.tvg_id}"')
        if stream.tvg_name:
            attrs.append(f'tvg-name="{stream.tvg_name}"')
        if stream.tvg_logo:
            attrs.append(f'tvg-logo="{stream.tvg_logo}"')
        if stream.group_title:
            attrs.append(f'group-title="{stream.group_title}"')
        if stream.tvg_language:
            attrs.append(f'tvg-language="{stream.tvg_language}"')
        if stream.tvg_country:
            attrs.append(f'tvg-country="{stream.tvg_country}"')

        attr_str = ' '.join(attrs)
        if attr_str:
            lines.append(f'#EXTINF:-1 {attr_str},{stream.name}')
        else:
            lines.append(f'#EXTINF:-1,{stream.name}')
        lines.append(stream.url)

    return "\n".join(lines) + "\n"


def to_json(streams: List[Stream], indent: int = 2) -> str:
    """
    Convert a list of streams to JSON format.

    Args:
        streams: List of Stream objects.
        indent: JSON indentation level.

    Returns:
        JSON-formatted string.
    """
    data = {
        "metadata": {
            "generator": "ALL-IN-ONE IPTV Engine v2.0.0",
            "total_streams": len(streams),
        },
        "streams": [asdict(s) for s in streams],
    }
    return json.dumps(data, indent=indent, ensure_ascii=False)
