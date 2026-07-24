"""
Grouper — Groups streams by country or category.
"""

from typing import Dict, List
from .parser import Stream


# Common country code to name mapping
COUNTRY_CODES: Dict[str, str] = {
    "US": "United States", "GB": "United Kingdom", "CA": "Canada",
    "AU": "Australia", "IN": "India", "DE": "Germany", "FR": "France",
    "ES": "Spain", "IT": "Italy", "BR": "Brazil", "MX": "Mexico",
    "JP": "Japan", "KR": "South Korea", "CN": "China", "RU": "Russia",
    "TR": "Turkey", "AR": "Argentina", "NL": "Netherlands", "PT": "Portugal",
    "PL": "Poland", "SE": "Sweden", "NO": "Norway", "DK": "Denmark",
    "FI": "Finland", "BE": "Belgium", "AT": "Austria", "CH": "Switzerland",
    "GR": "Greece", "CZ": "Czech Republic", "RO": "Romania", "HU": "Hungary",
    "BG": "Bulgaria", "HR": "Croatia", "RS": "Serbia", "UA": "Ukraine",
    "EG": "Egypt", "SA": "Saudi Arabia", "AE": "UAE", "PK": "Pakistan",
    "BD": "Bangladesh", "TH": "Thailand", "VN": "Vietnam", "ID": "Indonesia",
    "PH": "Philippines", "MY": "Malaysia", "NG": "Nigeria", "ZA": "South Africa",
    "KE": "Kenya", "GH": "Ghana", "CO": "Colombia", "PE": "Peru",
    "CL": "Chile", "VE": "Venezuela",
}


def group_by_country(streams: List[Stream]) -> Dict[str, List[Stream]]:
    """
    Group streams by their country attribute.

    Uses tvg_country field, falls back to group_title analysis,
    and defaults to 'Uncategorized' for streams with no country info.

    Args:
        streams: List of Stream objects.

    Returns:
        Dictionary mapping country names to lists of streams.
    """
    groups: Dict[str, List[Stream]] = {}

    for stream in streams:
        country = _extract_country(stream)
        if country not in groups:
            groups[country] = []
        groups[country].append(stream)

    return groups


def _extract_country(stream: Stream) -> str:
    """Extract country name from a stream's metadata."""
    # Try tvg_country first
    if stream.tvg_country:
        code = stream.tvg_country.strip().upper()
        if code in COUNTRY_CODES:
            return COUNTRY_CODES[code]
        # Might already be a full name
        if len(code) > 2:
            return stream.tvg_country.strip().title()
        return code

    # Try group_title for country hints
    if stream.group_title:
        gt = stream.group_title.strip()
        # Check if group title matches a country code
        gt_upper = gt.upper()
        if gt_upper in COUNTRY_CODES:
            return COUNTRY_CODES[gt_upper]
        # Check if it contains a country name
        for code, name in COUNTRY_CODES.items():
            if name.lower() in gt.lower():
                return name
        return gt

    return "Uncategorized"


def group_by_category(streams: List[Stream]) -> Dict[str, List[Stream]]:
    """Group streams by their group_title (category)."""
    groups: Dict[str, List[Stream]] = {}

    for stream in streams:
        cat = stream.group_title.strip() if stream.group_title else "General"
        if cat not in groups:
            groups[cat] = []
        groups[cat].append(stream)

    return groups
