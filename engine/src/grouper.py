from typing import List, Dict
from .parser import Stream

class Grouper:
    @staticmethod
    def group_by_category(streams: List[Stream]) -> Dict[str, List[Stream]]:
        groups = {}
        for s in streams:
            cat = s.group_title or "Uncategorized"
            if cat not in groups:
                groups[cat] = []
            groups[cat].append(s)
        return groups
