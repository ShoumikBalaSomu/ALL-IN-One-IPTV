"""
Fuzzy channel search engine.
"""

from typing import List, Dict, Any
from .utils import normalize_channel_name


class ChannelSearchEngine:
    """In-memory channel search and filter engine."""

    def __init__(self, channels: List[Dict[str, Any]] | None = None):
        self.channels = channels or []

    def set_channels(self, channels: List[Dict[str, Any]]) -> None:
        self.channels = channels

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search channels by name or group matching query."""
        if not query:
            return self.channels
        norm_query = normalize_channel_name(query)
        results = []
        for ch in self.channels:
            name = ch.get("name", "")
            group = ch.get("group", "")
            norm_name = normalize_channel_name(name)
            if norm_query in norm_name or norm_query in group.lower():
                results.append(ch)
        return results

    def filter_by_country(self, country: str) -> List[Dict[str, Any]]:
        """Filter channels by country/group."""
        if not country:
            return self.channels
        c_lower = country.lower()
        return [ch for ch in self.channels if c_lower in str(ch.get("group", "")).lower()]
