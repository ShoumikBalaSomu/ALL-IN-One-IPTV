"""
Utility functions for logging, text normalization, and string operations.
"""

import logging
import re
from urllib.parse import urlparse
from rich.logging import RichHandler
import structlog


def setup_logging():
    """Configure structured and rich logging."""
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    return structlog.get_logger()


logger = setup_logging()


def normalize_channel_name(name: str) -> str:
    """Clean and normalize channel name by stripping resolution/quality tags."""
    if not name:
        return ""
    # Remove resolution / quality / country bracketed tags like [HD], (UK), 1080p, etc.
    cleaned = re.sub(
        r"\[.*?\]|\(.*?\)|1080p|720p|4k|uhd|fhd|hd|sd|60fps|hevc",
        "",
        name,
        flags=re.IGNORECASE,
    )
    # Remove extra punctuation / whitespace
    cleaned = re.sub(r"\s+", " ", cleaned).strip().lower()
    return cleaned


def url_to_host(url: str) -> str:
    """Extract scheme + host from URL."""
    if not url:
        return ""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def detect_country_from_group(group: str) -> str:
    """Helper to detect country from group string."""
    if not group:
        return "Uncategorized"
    g_lower = group.lower().strip()

    country_map = {
        "bd": "Bangladesh",
        "bangladesh": "Bangladesh",
        "in": "India",
        "india": "India",
        "us": "United States",
        "usa": "United States",
        "american": "United States",
        "uk": "United Kingdom",
        "br": "Brazil",
        "brazil": "Brazil",
        "movies": "Movies",
        "sports": "Sports",
    }
    return country_map.get(g_lower, group.title())


def has_special_headers(stream_dict: dict) -> bool:
    """Check if stream dictionary or URL contains special HTTP headers or parameters."""
    url = stream_dict.get("url", "")
    vlc_opts = stream_dict.get("vlc_opts", [])
    if "token=" in url or "Cookie:" in str(vlc_opts) or "User-Agent" in str(vlc_opts):
        return True
    return False


def sanitize_text(text: str | None) -> str:
    """Sanitize string input."""
    if not text:
        return "Unknown"
    return text.strip()
