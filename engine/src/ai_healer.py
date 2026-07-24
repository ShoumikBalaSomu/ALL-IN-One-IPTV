from typing import List
from .parser import Stream

class AIHealer:
    def __init__(self, w1=0.4, w2=0.4, w3=0.2, max_latency=5000):
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3
        self.max_latency = max_latency
        
    def calculate_qrs(self, status: bool, latency: float, previous_score: float) -> float:
        S = 1.0 if status else 0.0
        L = min(latency, self.max_latency)
        latency_factor = max(0.0, 1 - (L / self.max_latency))
        score = (self.w1 * S) + (self.w2 * latency_factor) + (self.w3 * previous_score)
        return min(1.0, max(0.0, score))
        
    def heal_stream(self, stream: Stream, latency: float, status: bool) -> Stream:
        stream.qrs_score = self.calculate_qrs(status, latency, stream.qrs_score)
        if not status and stream.fallbacks:
            best_fallback = stream.fallbacks.pop(0)
            stream.fallbacks.append(stream.url)
            stream.url = best_fallback
        return stream
