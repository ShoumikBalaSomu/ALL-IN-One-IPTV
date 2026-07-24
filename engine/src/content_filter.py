"""
Content Filter — Parental controls and NSFW stream filter.
"""

import re
from typing import List, Dict, Any
from .parser import Stream
from .utils import logger


BLOCK_KEYWORDS: list[str] = [
    "xxx", "adult", "18+", "porn", "erotic",
    "playboy", "penthouse", "brazzers",
]


class ContentFilter:
    """Parental control and PIN-protected content filter."""

    def __init__(self, system_pin: str = "0171"):
        self.system_pin = system_pin
        self.keywords = list(BLOCK_KEYWORDS)
        self.pattern = re.compile("|".join(re.escape(kw) for kw in self.keywords), re.IGNORECASE)

    def verify_pin(self, pin: str) -> bool:
        return pin == self.system_pin

    def is_explicit(self, channel: Dict[str, Any]) -> bool:
        searchable = f"{channel.get('name', '')} {channel.get('group', '')}"
        return bool(self.pattern.search(searchable))

    def filter_channels(self, channels: List[Dict[str, Any]], pin_unlocked: bool = False) -> List[Dict[str, Any]]:
        if pin_unlocked:
            return channels
        return [ch for ch in channels if not self.is_explicit(ch)]


def filter_content(
    streams: List[Stream],
    blocked_keywords: list[str] | None = None,
    allow_keywords: list[str] | None = None,
) -> List[Stream]:
    keywords = list(BLOCK_KEYWORDS)
    if blocked_keywords:
        keywords.extend(blocked_keywords)

    pattern = re.compile("|".join(re.escape(kw) for kw in keywords), re.IGNORECASE)
    filtered: List[Stream] = []
    removed = 0

    for stream in streams:
        searchable = f"{stream.name} {stream.group_title}"
        if pattern.search(searchable):
            removed += 1
            continue

        if allow_keywords:
            allow_pattern = re.compile("|".join(re.escape(kw) for kw in allow_keywords), re.IGNORECASE)
            if not allow_pattern.search(searchable):
                removed += 1
                continue

        filtered.append(stream)

    if removed > 0:
        logger.info(f"Content filter removed {removed} streams")

    return filtered
