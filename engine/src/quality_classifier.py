"""
Quality Classifier — Auto-classify stream resolution & framerate.
"""

import re
from typing import Optional, Dict, Any


_QUALITY_PATTERNS = [
    (re.compile(r"\b(4K|UHD|2160p?)\b", re.IGNORECASE), "4K"),
    (re.compile(r"\b(FHD|1080p?)\b", re.IGNORECASE), "FHD"),
    (re.compile(r"\b(HD|720p?)\b", re.IGNORECASE), "HD"),
    (re.compile(r"\b(SD|480p?|360p?)\b", re.IGNORECASE), "SD"),
]


class StreamQualityClassifier:
    """Classifies resolution and framerate of stream channels."""

    def classify_channel(self, channel: Dict[str, Any]) -> Dict[str, Any]:
        name = channel.get("name", "")
        quality = detect_quality(name) or "SD"
        is_60fps = "60fps" in name.lower() or "60" in name.lower()

        res = dict(channel)
        res["quality"] = quality
        res["is_60fps"] = is_60fps
        return res


def detect_quality(name: str) -> Optional[str]:
    for pattern, label in _QUALITY_PATTERNS:
        if pattern.search(name):
            return label
    return None


def classify_quality(name: str, existing_group: str = "") -> str:
    quality = detect_quality(name)
    if not existing_group:
        return quality or "General"
    if quality and quality.upper() not in existing_group.upper():
        return f"{existing_group} [{quality}]"
    return existing_group
