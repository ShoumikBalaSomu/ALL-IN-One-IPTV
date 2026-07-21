"""
Channel Folder — Fold duplicate channels into single entries with multiple URLs.

When the same channel appears from multiple sources, fold them into a single
channel entry that lists all stream URLs. The player can then try each URL
until one works.
"""

import re
from collections import defaultdict

from .utils import setup_logging, normalize_channel_name

logger = setup_logging("engine.folder")


class ChannelFolder:
    """Fold channels with similar names into groups with multiple URLs."""

    def fold(self, channels: list[dict]) -> list[dict]:
        """Fold channels by normalized name within each group.

        Returns a list where each entry represents a unique channel,
        potentially with multiple stream URLs.
        """
        # Group by (country_group, normalized_name)
        folded_map: dict[str, dict] = {}

        for ch in channels:
            group = ch.get("group", "Uncategorized")
            norm_name = normalize_channel_name(ch.get("name", ""))

            if not norm_name:
                norm_name = "unknown"

            key = f"{group}|||{norm_name}"

            if key not in folded_map:
                # First occurrence — create folded entry
                folded_map[key] = {
                    "name": ch.get("name", "Unknown"),
                    "tvg_id": ch.get("tvg_id", ""),
                    "tvg_name": ch.get("tvg_name", ""),
                    "tvg_country": ch.get("tvg_country", ""),
                    "tvg_logo": ch.get("tvg_logo", ""),
                    "group": group,
                    "group_title": ch.get("group_title", ""),
                    "url": ch["url"],
                    "urls": [ch["url"]],  # All URLs for this channel
                    "extinf": ch.get("extinf", ""),
                    "vlc_opts": ch.get("vlc_opts", []),
                    "kodi_props": ch.get("kodi_props", []),
                    "http_headers": ch.get("http_headers", []),
                    "has_cookies": ch.get("has_cookies", False),
                    "_norm_name": norm_name,
                    "_sources": [ch.get("source", "")],
                }
            else:
                # Merge additional URL
                existing = folded_map[key]
                existing["urls"].append(ch["url"])
                existing["_sources"].append(ch.get("source", ""))

                # Prefer entries with logos
                if not existing["tvg_logo"] and ch.get("tvg_logo"):
                    existing["tvg_logo"] = ch["tvg_logo"]

                # Prefer entries with TVG IDs
                if not existing["tvg_id"] and ch.get("tvg_id"):
                    existing["tvg_id"] = ch["tvg_id"]

                # Track if any URL has cookies
                if ch.get("has_cookies"):
                    existing["has_cookies"] = True

                # Merge VLC opts (unique)
                for opt in ch.get("vlc_opts", []):
                    if opt not in existing["vlc_opts"]:
                        existing["vlc_opts"].append(opt)

        result = list(folded_map.values())

        # Sort by group, then name
        result.sort(key=lambda c: (c["group"], c["_norm_name"]))

        folded_count = sum(1 for c in result if len(c["urls"]) > 1)
        logger.info(
            f"Folding: {len(channels)} entries → {len(result)} channels "
            f"({folded_count} with multiple URLs)"
        )

        return result

    def unfold(self, folded_channels: list[dict]) -> list[dict]:
        """Unfold folded channels back to flat list (one URL per entry).

        Useful for exporting to standard M3U format.
        """
        flat = []
        for ch in folded_channels:
            urls = ch.get("urls", [ch["url"]])
            for i, url in enumerate(urls):
                entry = dict(ch)
                entry["url"] = url
                if i == 0:
                    entry["name"] = ch["name"]
                else:
                    # Append URL count for non-primary URLs
                    entry["name"] = ch["name"]
                flat.append(entry)
        return flat