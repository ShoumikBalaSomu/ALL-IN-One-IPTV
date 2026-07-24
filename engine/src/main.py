import asyncio
from .collector import Collector
from .parser import M3UParser
from .deduplicator import Deduplicator
from .content_filter import ContentFilter
from .quality_classifier import QualityClassifier
from .verifier import Verifier
from .ai_healer import AIHealer

async def main():
    sources = ["http://example.com/test.m3u"]
    collector = Collector(sources)
    raw_m3u = await collector.collect()
    
    streams = M3UParser.parse(raw_m3u)
    
    deduped = Deduplicator.deduplicate(streams)
    
    filterer = ContentFilter()
    filtered = filterer.filter(deduped)
    
    for s in filtered:
        QualityClassifier.classify(s)
        
    verifier = Verifier()
    verified_results = await verifier.verify_all(filtered)
    
    healer = AIHealer()
    final_streams = []
    for stream, is_valid, latency in verified_results:
        healed_stream = healer.heal_stream(stream, latency, is_valid)
        final_streams.append(healed_stream)
        
    final_m3u = M3UParser.generate(final_streams)
    print("Pipeline Complete")
    return final_m3u

if __name__ == "__main__":
    asyncio.run(main())
