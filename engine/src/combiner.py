"""
Combiner — Export latency-ranked combined playlists grouped by country with fallback stream mirrors.
"""

import os
from typing import List, Dict

from .parser import Stream
from .grouper import group_by_country
from .utils import logger


def export_combined(streams: List[Stream], output_path: str) -> str:
    """
    Export all streams to a single M3U file, grouped by country with latency-ranked fallback mirrors.

    Args:
        streams: List of Stream objects to export.
        output_path: Path to the output .m3u file.

    Returns:
        The output file path.
    """
    grouped = group_by_country(streams)

    lines = ["#EXTM3U"]
    lines.append(f"# ALL-IN-ONE IPTV — Smart Latency-Ranked Playlist")
    lines.append(f"# Total folded channels: {len(streams)}")
    lines.append(f"# Countries/Categories: {len(grouped)}")
    lines.append("")

    for country in sorted(grouped.keys()):
        country_streams = grouped[country]
        lines.append(f"# ═══════════════════════════════════════")
        lines.append(f"# {country.upper()} ({len(country_streams)} channels)")
        lines.append(f"# ═══════════════════════════════════════")

        for stream in country_streams:
            extinf_parts = ['#EXTINF:-1']
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

            if attrs:
                extinf_parts.append(' ' + ' '.join(attrs))

            extinf_parts.append(f',{stream.name}')
            lines.append(''.join(extinf_parts))

            # Include VLC options and fallback mirrors
            if stream.vlc_opts:
                lines.extend(stream.vlc_opts)

            if stream.fallback_urls:
                for fb in stream.fallback_urls:
                    lines.append(f"#EXTVLCOPT:fallback={fb}")

            lines.append(stream.url)

        lines.append("")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    logger.info(f"Exported {len(streams)} folded channels to {output_path}")
    return output_path
