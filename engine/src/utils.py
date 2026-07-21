"""
Utility functions for the IPTV Engine.
"""

import logging
import re
import hashlib
from urllib.parse import urlparse


def setup_logging(name: str = "engine", level: int = logging.INFO) -> logging.Logger:
    """Configure and return a logger instance."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger


logger = setup_logging()


def normalize_channel_name(name: str) -> str:
    """Normalize channel name for fuzzy matching.

    Removes quality tags, country codes, and special characters.
    """
    normalized = name.strip()

    # Remove country codes in parentheses FIRST (before lowercasing)
    normalized = re.sub(r'\([A-Z]{2,4}\)', '', normalized)

    # Lowercase
    normalized = normalized.lower()

    # Remove common quality/resolution tags
    tags = [
        r'\[HD\]', r'\[FHD\]', r'\[SD\]', r'\[4K\]', r'\[8K\]', r'\[RAW\]',
        r'\[IPTV\]', r'\[SAT\]', r'\[CABLE\]',
        r'\(HD\)', r'\(FHD\)', r'\(SD\)',
        r'1080p', r'720p', r'480p', r'4K', r'8K',
        r'HEVC', r'H265', r'H264', r'AV1',
    ]
    for tag in tags:
        normalized = re.sub(tag, '', normalized, flags=re.IGNORECASE)

    # Remove standalone quality words
    for word in ['hd', 'fhd', 'sd', 'uhd']:
        normalized = re.sub(r'\b' + word + r'\b', '', normalized)

    # Remove special characters, keep alphanumeric and spaces
    normalized = re.sub(r'[^a-z0-9\s]', '', normalized)

    # Collapse multiple spaces
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    return normalized


def url_to_host(url: str) -> str:
    """Extract host (scheme + netloc) from URL for group health checking."""
    try:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    except Exception:
        return url


def url_hash(url: str) -> str:
    """Generate a short hash for URL deduplication tracking."""
    return hashlib.md5(url.encode()).hexdigest()[:12]


def detect_country_from_group(group: str) -> str:
    """Try to detect country code/name from group-title field."""
    group = group.strip().lower()

    # Check for genre-based groups FIRST (before country codes)
    # This prevents "movies" matching "es" (Spain)
    genre_map = {
        'movie': 'Movies', 'movies': 'Movies', 'film': 'Movies', 'cinema': 'Movies',
        'series': 'Series', 'tv show': 'Series', 'drama': 'Series',
        'sport': 'Sports', 'sports': 'Sports', 'cricket': 'Sports', 'football': 'Sports',
        'news': 'News', 'news channel': 'News',
        'music': 'Music', 'music channel': 'Music',
        'kids': 'Kids', 'children': 'Kids', 'cartoon': 'Kids', 'animation': 'Kids',
        'religious': 'Religious', 'islam': 'Religious', 'hindu': 'Religious',
        'documentary': 'Documentary', 'doc': 'Documentary',
        'adult': 'Adult', 'xxx': 'Adult', 'ppv': 'Adult',
        'ott': 'OTT', 'netflix': 'OTT', 'prime': 'OTT', 'hotstar': 'OTT',
    }

    # Check full match first for genres
    if group in genre_map:
        return genre_map[group]

    # Check for country/full name matches (longer keys first to avoid partial matches)
    country_map = {
        'bangladesh': 'Bangladesh', 'bd': 'Bangladesh',
        'india': 'India', 'in': 'India',
        'pakistan': 'Pakistan', 'pk': 'Pakistan',
        'united states': 'United States', 'usa': 'United States', 'american': 'United States', 'us': 'United States',
        'united kingdom': 'United Kingdom', 'uk': 'United Kingdom', 'british': 'United Kingdom', 'english': 'United Kingdom',
        'brazil': 'Brazil', 'portuguese': 'Brazil', 'br': 'Brazil',
        'china': 'China', 'chinese': 'China', 'cn': 'China',
        'japan': 'Japan', 'japanese': 'Japan', 'jp': 'Japan',
        'south korea': 'South Korea', 'korea': 'South Korea', 'korean': 'South Korea', 'kr': 'South Korea',
        'germany': 'Germany', 'german': 'Germany', 'de': 'Germany',
        'france': 'France', 'french': 'France', 'fr': 'France',
        'spain': 'Spain', 'spanish': 'Spain', 'es': 'Spain',
        'italy': 'Italy', 'italian': 'Italy', 'it': 'Italy',
        'russia': 'Russia', 'russian': 'Russia', 'ru': 'Russia',
        'turkey': 'Turkey', 'turkish': 'Turkey', 'tr': 'Turkey',
        'argentina': 'Argentina', 'ar': 'Argentina',
        'mexico': 'Mexico', 'mx': 'Mexico',
        'canada': 'Canada', 'ca': 'Canada',
        'australia': 'Australia', 'au': 'Australia',
        'vietnam': 'Vietnam', 'vn': 'Vietnam',
        'thailand': 'Thailand', 'th': 'Thailand',
        'malaysia': 'Malaysia', 'my': 'Malaysia',
        'singapore': 'Singapore', 'sg': 'Singapore',
        'indonesia': 'Indonesia', 'id': 'Indonesia',
        'philippines': 'Philippines', 'ph': 'Philippines',
        'uae': 'UAE', 'arabic': 'Middle East', 'ae': 'UAE',
        'saudi arabia': 'Saudi Arabia', 'saudi': 'Saudi Arabia', 'sa': 'Saudi Arabia',
        'egypt': 'Egypt', 'eg': 'Egypt',
        'nigeria': 'Nigeria', 'ng': 'Nigeria',
        'south africa': 'South Africa', 'za': 'South Africa',
    }

    # Full match first
    if group in country_map:
        return country_map[group]

    # For 2-letter codes, only match if the group is exactly that code
    # (avoid matching "es" in "movies")
    if len(group) == 2 and group in country_map:
        return country_map[group]

    # For longer groups, check if any country name is a substring
    # Sort by length descending to prefer longer (more specific) matches
    for key in sorted(country_map.keys(), key=len, reverse=True):
        if len(key) > 2 and key in group:
            return country_map[key]

    # Finally, check genre partial matches
    for key in sorted(genre_map.keys(), key=len, reverse=True):
        if key in group:
            return genre_map[key]

    return group.title() if group else "Uncategorized"


def has_special_headers(channel: dict) -> bool:
    """Check if a channel has cookies, tokens, or special HTTP headers."""
    url = channel.get("url", "").lower()
    vlc_opts = channel.get("vlc_opts", [])

    # URL contains query parameters (often tokens/cookies)
    if "?" in url:
        return True

    # VLC opts contain cookie/auth headers
    cookie_keywords = ["cookie", "token", "auth", "authorization", "referer", "user-agent"]
    for opt in vlc_opts:
        opt_lower = opt.lower()
        if any(kw in opt_lower for kw in cookie_keywords):
            return True

    return False


def sanitize_text(text: str) -> str:
    """Sanitize text for safe M3U output."""
    if not text:
        return "Unknown"
    # Remove null bytes and control characters
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return text.strip()