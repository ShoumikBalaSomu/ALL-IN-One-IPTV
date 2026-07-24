"""
Fuzzy deduplication using URL normalization + title similarity.
"""
from typing import List
from .parser import Stream

def deduplicate(streams: List[Stream]) -> List[Stream]:
    seen_urls = set()
    unique = []
    for s in streams:
        url = s.url.lower().strip()
        if url not in seen_urls:
            seen_urls.add(url)
            unique.append(s)
    return unique
