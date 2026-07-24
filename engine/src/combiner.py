from typing import List
from .parser import Stream, M3UParser

class Combiner:
    @staticmethod
    def combine(stream_lists: List[List[Stream]]) -> str:
        combined = []
        for lst in stream_lists:
            combined.extend(lst)
        return M3UParser.generate(combined)
