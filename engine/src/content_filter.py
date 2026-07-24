"""
Content Classification & Parental Control Filter Engine.
Identifies adult/explicit channels and enforces system PIN verification (default PIN: 0171).
"""

import re

EXPLICIT_KEYWORDS = [
    'xxx', 'adult', '18+', 'playboy', 'penthouse', 'brazzers', 'hustler',
    'erotic', 'redlight', 'nsfw', 'porn', 'sensual', 'vivid', 'dorcel'
]

class ContentFilter:
    """Classifies and filters content based on explicit keywords and PIN status."""

    def __init__(self, system_pin: str = "0171"):
        self.system_pin = system_pin
        self.explicit_regex = re.compile(
            r'\b(' + '|'.join(EXPLICIT_KEYWORDS) + r')\b', re.IGNORECASE
        )

    def is_explicit(self, channel: dict) -> bool:
        """Check if a channel contains explicit content based on name or group."""
        name = channel.get('name', '')
        group = channel.get('group', '')
        text = f"{name} {group}"
        return bool(self.explicit_regex.search(text))

    def verify_pin(self, input_pin: str) -> bool:
        """Verify if user provided PIN matches system PIN."""
        return str(input_pin).strip() == self.system_pin

    def filter_channels(self, channels: list[dict], pin_unlocked: bool = False) -> list[dict]:
        """Filter list of channels. Hides explicit content unless pin_unlocked is True."""
        if pin_unlocked:
            return channels
        return [ch for ch in channels if not self.is_explicit(ch)]

    def sanitize_playlist_output(self, channels: list[dict], pin_unlocked: bool = False) -> tuple[list[dict], list[dict]]:
        """Separate channel list into safe channels and explicit channels."""
        safe = []
        explicit = []
        for ch in channels:
            if self.is_explicit(ch):
                explicit.append(ch)
            else:
                safe.append(ch)
        return safe, explicit
