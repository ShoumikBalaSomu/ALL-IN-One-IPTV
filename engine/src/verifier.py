import asyncio
from typing import List
from .parser import Stream
from .utils import get_logger

logger = get_logger(__name__)

class Verifier:
    def __init__(self, max_workers: int = 50):
        self.max_workers = max_workers
        self.semaphore = asyncio.Semaphore(max_workers)

    async def verify_single(self, stream: Stream) -> tuple[Stream, bool, float]:
        async with self.semaphore:
            # Mock verification
            await asyncio.sleep(0.01)
            is_valid = True
            latency = 150.0
            if "dead" in stream.url:
                is_valid = False
                latency = 5000.0
            return stream, is_valid, latency

    async def verify_all(self, streams: List[Stream]) -> List[tuple[Stream, bool, float]]:
        tasks = [self.verify_single(s) for s in streams]
        return await asyncio.gather(*tasks)
