from typing import List, Dict
from .parser import Stream

class Deduplicator:
    @staticmethod
    def deduplicate(streams: List[Stream]) -> List[Stream]:
        unique_streams: Dict[str, Stream] = {}
        for s in streams:
            key = f"{s.tvg_id}-{s.name}".lower()
            if key in unique_streams:
                if s.url not in unique_streams[key].fallbacks and s.url != unique_streams[key].url:
                    unique_streams[key].fallbacks.append(s.url)
            else:
                unique_streams[key] = s
        return list(unique_streams.values())
