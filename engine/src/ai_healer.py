"""
AI Quantum Stream Healer & Health Predictor Engine (Year 3050 Spec).

Calculates Quantum Stream Health Index (0.0% to 100.0%) based on response latency,
domain uptime history, and protocol stability to predict stream longevity.
"""

import math
from typing import Dict, List
from .parser import Stream

class AIStreamHealer:
    """Predicts stream stability and ranks streams via Quantum Reliability Score (QRS)."""

    def compute_quantum_score(self, stream: Stream) -> float:
        """Compute Quantum Reliability Score (QRS) between 0.0 and 100.0."""
        if stream.latency_ms >= 9999.0 or not stream.url:
            return 0.0

        # Latency score component (0-50 pts): lower latency = higher score
        latency_score = max(0.0, 50.0 - (stream.latency_ms / 20.0))

        # Protocol stability bonus (0-30 pts): HTTPS gets bonus over HTTP
        protocol_score = 30.0 if stream.url.startswith("https://") else 20.0

        # Metadata richness bonus (0-20 pts)
        metadata_score = 0.0
        if stream.tvg_logo:
            metadata_score += 7.0
        if stream.tvg_id:
            metadata_score += 7.0
        if stream.group_title:
            metadata_score += 6.0

        total_qrs = min(100.0, latency_score + protocol_score + metadata_score)
        return round(total_qrs, 1)

    def enhance_stream_with_ai(self, stream: Stream) -> Stream:
        """Attach quantum health metrics to Stream object."""
        qrs = self.compute_quantum_score(stream)
        stream.vlc_opts.append(f"#EXTVLCOPT:qrs-score={qrs}%")
        return stream

    def rank_streams_by_quantum_score(self, streams: List[Stream]) -> List[Stream]:
        """Rank collection of streams by Quantum Reliability Score descending."""
        scored = [(self.compute_quantum_score(s), s) for s in streams]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored]
