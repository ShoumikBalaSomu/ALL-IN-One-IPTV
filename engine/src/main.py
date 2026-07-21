"""
ALL-IN-One-IPTV Engine
Modular playlist aggregation, combination, and verification system.

Usage:
    python main.py              # Run full pipeline
    python main.py --collect    # Only collect playlists
    python main.py --verify     # Only verify links
    python main.py --input dir  # Custom input directory
"""

from .collector import PlaylistCollector
from .parser import M3UParser
from .combiner import PlaylistCombiner
from .deduplicator import Deduplicator
from .grouper import CountryGrouper
from .folder import ChannelFolder
from .verifier import LinkVerifier
from .utils import setup_logging

logger = setup_logging("engine.main")


async def run_pipeline(
    playlist_urls: list[str] | None = None,
    input_dir: str = "input",
    output_dir: str = "output",
    verify_links: bool = True,
    concurrency: int = 100,
    decrypt_key: str | None = None,
):
    """Run the full aggregation pipeline."""
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Collect
    logger.info("=" * 60)
    logger.info("STEP 1: Collecting playlists...")
    logger.info("=" * 60)
    collector = PlaylistCollector(playlist_urls, decrypt_key)
    raw_content = await collector.collect(input_dir)
    logger.info(f"Collected {len(raw_content)} playlist sources")

    # Step 2: Parse
    logger.info("=" * 60)
    logger.info("STEP 2: Parsing M3U content...")
    logger.info("=" * 60)
    parser = M3UParser()
    all_channels = parser.parse_all(raw_content)
    logger.info(f"Parsed {len(all_channels)} total channel entries")

    # Step 3: Deduplicate
    logger.info("=" * 60)
    logger.info("STEP 3: Deduplicating channels...")
    logger.info("=" * 60)
    deduplicator = Deduplicator()
    unique_channels = deduplicator.deduplicate(all_channels)
    logger.info(f"After dedup: {len(unique_channels)} unique URLs")

    # Step 4: Combine & Group by Country
    logger.info("=" * 60)
    logger.info("STEP 4: Grouping by country...")
    logger.info("=" * 60)
    grouper = CountryGrouper()
    grouped = grouper.group(unique_channels)
    countries = list(grouped.keys())
    logger.info(f"Found {len(countries)} countries/groups: {', '.join(countries[:10])}...")

    # Step 5: Fold Duplicates
    logger.info("=" * 60)
    logger.info("STEP 5: Folding duplicate channels...")
    logger.info("=" * 60)
    folder = ChannelFolder()
    folded = folder.fold(unique_channels)
    logger.info(f"After folding: {len(folded)} channel groups")

    # Step 6: Export Combined (unchecked)
    combiner = PlaylistCombiner()
    combined_path = combiner.export(folded, output_dir, "combined_by_country.m3u")
    logger.info(f"✅ Combined playlist: {combined_path}")

    # Step 7: Verify Links (optional but recommended)
    if verify_links:
        logger.info("=" * 60)
        logger.info("STEP 7: Verifying link health (this may take几分钟)...")
        logger.info("=" * 60)
        verifier = LinkVerifier(concurrency=concurrency)
        verified = await verifier.verify(folded)
        verified_path = combiner.export(verified, output_dir, "checked_combined_by_country.m3u")
        logger.info(f"✅ Verified playlist: {verified_path}")
        logger.info(f"   Valid channels: {len(verified)}/{len(folded)}")
    else:
        verified = folded

    return {
        "total_parsed": len(all_channels),
        "unique_urls": len(unique_channels),
        "folded_groups": len(folded),
        "verified": len(verified) if verify_links else None,
        "countries": len(countries),
        "combined_file": combined_path,
        "verified_file": combined_path.replace("combined_by_country.m3u", "checked_combined_by_country.m3u") if verify_links else None,
    }


def main():
    import asyncio
    import argparse

    parser = argparse.ArgumentParser(description="ALL-IN-One-IPTV Engine")
    parser.add_argument("--input", default="input", help="Input directory for local playlists")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--no-verify", action="store_true", help="Skip link verification")
    parser.add_argument("--concurrency", type=int, default=100, help="Concurrent verification requests")
    parser.add_argument("--decrypt-key", help="Hex key for decrypting .enc playlists")
    args = parser.parse_args()

    stats = asyncio.run(
        run_pipeline(
            input_dir=args.input,
            output_dir=args.output,
            verify_links=not args.no_verify,
            concurrency=args.concurrency,
            decrypt_key=args.decrypt_key,
        )
    )

    logger.info("")
    logger.info("=" * 60)
    logger.info("PIPELINE COMPLETE")
    logger.info("=" * 60)
    for key, value in stats.items():
        logger.info(f"  {key}: {value}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()