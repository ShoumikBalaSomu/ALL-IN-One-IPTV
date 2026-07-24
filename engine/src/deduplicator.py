"""
Smart Channel Merger & Host Latency Ranker.

Folds duplicate channels into a single entry with latency-ranked fallback stream URLs.
"""

from typing import List, Dict
from collections import defaultdict
from .parser import Stream
from .utils import normalize_channel_name, logger


def deduplicate(streams: List[Stream]) -> List[Stream]:
    """
    Smartly merge and fold channels by normalized name.
    Ranks fallback stream URLs by lowest response latency (ms).
    """
    if not streams:
        return []

    # 1. Exact URL Deduplication
    seen_urls = set()
    url_unique_streams = []
    for s in streams:
        url_clean = s.url.strip()
        if url_clean and url_clean not in seen_urls:
            seen_urls.add(url_clean)
            url_unique_streams.append(s)

    # 2. Smart Channel Folding & Latency Ranking
    channel_groups: Dict[str, List[Stream]] = defaultdict(list)
    for s in url_unique_streams:
        norm_name = normalize_channel_name(s.name)
        key = norm_name if norm_name else s.name.lower().strip()
        channel_groups[key].append(s)

    merged_streams: List[Stream] = []

    for key, stream_list in channel_groups.items():
        # Sort stream list by latency_ms ascending (lowest ping first)
        stream_list.sort(key=lambda x: x.latency_ms)

        # Primary stream is the fastest responding host
        primary = stream_list[0]
        
        # Collect fallback URLs from remaining streams in latency order
        fallbacks = [s.url for s in stream_list[1:] if s.url != primary.url]
        primary.fallback_urls = fallbacks

        merged_streams.append(primary)

    logger.info(f"Smart Merger: Folded {len(streams)} raw links into {len(merged_streams)} latency-ranked channels.")
    return merged_streams
