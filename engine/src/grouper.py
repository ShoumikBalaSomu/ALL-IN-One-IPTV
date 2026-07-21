"""
Country Grouper — Group channels by detected country.
"""

from collections import defaultdict

from .utils import setup_logging

logger = setup_logging("engine.grouper")


class CountryGrouper:
    """Group channels by their detected country/group."""

    def group(self, channels: list[dict]) -> dict[str, list[dict]]:
        """Group channels by their 'group' field (country/category)."""
        grouped: dict[str, list[dict]] = defaultdict(list)

        for ch in channels:
            group = ch.get("group", "Uncategorized")
            grouped[group].append(ch)

        # Sort channels within each group by name
        for group in grouped:
            grouped[group].sort(key=lambda c: c.get("name", "").lower())

        logger.info(f"Grouped into {len(grouped)} countries/categories")
        return dict(grouped)

    def get_country_stats(self, channels: list[dict]) -> dict[str, int]:
        """Get channel count per country."""
        stats: dict[str, int] = defaultdict(int)
        for ch in channels:
            stats[ch.get("group", "Uncategorized")] += 1
        return dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))