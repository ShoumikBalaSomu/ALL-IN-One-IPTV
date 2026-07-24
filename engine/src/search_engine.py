from typing import List
from .parser import Stream

class SearchEngine:
    def __init__(self, streams: List[Stream]):
        self.streams = streams

    def search(self, query: str) -> List[Stream]:
        q = query.lower()
        return [s for s in self.streams if q in s.name.lower() or q in s.group_title.lower()]
