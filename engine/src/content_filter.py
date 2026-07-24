from typing import List
from .parser import Stream

class ContentFilter:
    def __init__(self, pin: str = "0171", blocked_keywords: List[str] = None):
        self.pin = pin
        self.blocked_keywords = blocked_keywords or ["adult", "xxx", "18+"]

    def filter(self, streams: List[Stream]) -> List[Stream]:
        filtered = []
        for s in streams:
            name_lower = s.name.lower()
            if any(kw in name_lower for kw in self.blocked_keywords):
                # Apply parental control
                s.name = f"[LOCKED] {s.name}"
                s.vlc_opts['pin'] = self.pin
            filtered.append(s)
        return filtered
