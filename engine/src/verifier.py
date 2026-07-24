"""
Verifier — Concurrent stream health checker.

Pings each stream URL with an HTTP HEAD request to determine
if it's still alive, respecting rate limits and timeouts.
"""

import asyncio
from typing import List

import aiohttp
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn

from .parser import Stream
from .utils import logger


async def check_stream(
    session: aiohttp.ClientSession,
    stream: Stream,
    timeout: int = 10,
) -> bool:
    """Check if a single stream URL is alive via HEAD request."""
    try:
        async with session.head(
            stream.url,
            timeout=aiohttp.ClientTimeout(total=timeout),
            ssl=False,
            allow_redirects=True,
        ) as resp:
            return resp.status < 400
    except (aiohttp.ClientError, asyncio.TimeoutError, Exception):
        return False


async def verify_streams(
    streams: List[Stream],
    workers: int = 25,
    timeout: int = 10,
) -> List[Stream]:
    """
    Verify a list of streams concurrently.

    Args:
        streams: List of Stream objects to verify.
        workers: Maximum concurrent verification requests.
        timeout: Per-stream timeout in seconds.

    Returns:
        List of streams that responded successfully.
    """
    if not streams:
        return []

    alive: List[Stream] = []
    semaphore = asyncio.Semaphore(workers)
    connector = aiohttp.TCPConnector(limit=workers, force_close=True)

    async with aiohttp.ClientSession(connector=connector) as session:

        async def bounded_check(stream: Stream) -> tuple[Stream, bool]:
            async with semaphore:
                result = await check_stream(session, stream, timeout)
                return stream, result

        tasks = [bounded_check(s) for s in streams]

        with Progress(
            SpinnerColumn(),
            TextColumn("[cyan]Verifying streams..."),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeRemainingColumn(),
        ) as progress:
            task_id = progress.add_task("Verifying", total=len(tasks))

            for coro in asyncio.as_completed(tasks):
                stream, is_alive = await coro
                if is_alive:
                    alive.append(stream)
                progress.advance(task_id)

    dead = len(streams) - len(alive)
    logger.info(f"Verification complete: {len(alive)} alive, {dead} dead")
    return alive
