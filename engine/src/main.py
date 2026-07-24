"""
ALL-IN-ONE IPTV Engine — Main Pipeline Orchestrator

Runs the complete aggregation pipeline:
  1. Collect playlists from remote sources + local files
  2. Parse all M3U content into structured Stream objects
  3. Deduplicate streams by URL normalization
  4. Group streams by country
  5. Classify stream quality (SD/HD/FHD/4K)
  6. Apply content filters
  7. Verify stream health (optional)
  8. Export to M3U and JSON formats

Usage:
    python -m engine.src                          # Full pipeline
    python -m engine.src --no-verify              # Skip verification
    python -m engine.src --output ./my_output     # Custom output dir
    python -m engine.src --workers 50             # Custom concurrency
"""

import asyncio
import argparse
import os
import sys
import time
from pathlib import Path
from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .collector import collect_all
from .parser import Stream
from .deduplicator import deduplicate
from .grouper import group_by_country
from .quality_classifier import classify_quality
from .content_filter import filter_content
from .verifier import verify_streams
from .folder import to_m3u, to_json
from .combiner import export_combined
from .utils import logger

console = Console()

BANNER = """
╔═══════════════════════════════════════════════════════════════╗
║        █████╗ ██╗     ██╗      ██╗███╗   ██╗ ██╗             ║
║       ██╔══██╗██║     ██║      ██║████╗  ██║███║             ║
║       ███████║██║     ██║█████╗██║██╔██╗ ██║╚██║             ║
║       ██╔══██║██║     ██║╚════╝██║██║╚██╗██║ ██║             ║
║       ██║  ██║███████╗███████╗ ██║██║ ╚████║ ██║             ║
║       ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝╚═╝             ║
║                   IPTV Engine v2.0.0                          ║
╚═══════════════════════════════════════════════════════════════╝
"""


async def run_pipeline(
    input_dir: str = "input",
    output_dir: str = "output",
    verify: bool = True,
    workers: int = 25,
    verify_timeout: int = 10,
) -> dict:
    """Run the full aggregation pipeline."""

    console.print(Text(BANNER, style="bold cyan"))
    start_time = time.time()

    os.makedirs(output_dir, exist_ok=True)

    # ── Step 1: Collect ─────────────────────────────────────────────
    console.rule("[bold blue]Step 1/7 · Collecting Playlists")
    all_streams = await collect_all(input_dir=input_dir)

    if not all_streams:
        console.print("[bold red]No streams collected! Exiting.")
        return {"status": "error", "reason": "no streams collected"}

    # ── Step 2: Deduplicate ─────────────────────────────────────────
    console.rule("[bold blue]Step 2/7 · Deduplicating")
    unique_streams = deduplicate(all_streams)
    logger.info(f"Deduplicated: {len(all_streams)} → {len(unique_streams)} streams")

    # ── Step 3: Classify Quality ────────────────────────────────────
    console.rule("[bold blue]Step 3/7 · Classifying Quality")
    for stream in unique_streams:
        stream.group_title = classify_quality(stream.name, stream.group_title)

    # ── Step 4: Content Filter ──────────────────────────────────────
    console.rule("[bold blue]Step 4/7 · Filtering Content")
    filtered = filter_content(unique_streams)
    logger.info(f"After filtering: {len(filtered)} streams")

    # ── Step 5: Group by Country ────────────────────────────────────
    console.rule("[bold blue]Step 5/7 · Grouping by Country")
    grouped = group_by_country(filtered)
    logger.info(f"Found {len(grouped)} countries/regions")

    # ── Step 6: Export Combined (all) ───────────────────────────────
    console.rule("[bold blue]Step 6/7 · Exporting Playlists")

    combined_path = os.path.join(output_dir, "combined_by_country.m3u")
    export_combined(filtered, combined_path)
    logger.info(f"  ✅ Combined M3U: {combined_path}")

    json_path = os.path.join(output_dir, "combined.json")
    json_content = to_json(filtered)
    Path(json_path).write_text(json_content, encoding="utf-8")
    logger.info(f"  ✅ JSON export: {json_path}")

    # ── Step 7: Verify (optional) ───────────────────────────────────
    verified_count = None
    if verify:
        console.rule("[bold blue]Step 7/7 · Verifying Stream Health")
        verified = await verify_streams(
            filtered,
            workers=workers,
            timeout=verify_timeout,
        )
        verified_count = len(verified)

        checked_path = os.path.join(output_dir, "checked_combined_by_country.m3u")
        export_combined(verified, checked_path)
        logger.info(f"  ✅ Verified M3U: {checked_path} ({verified_count}/{len(filtered)} alive)")
    else:
        console.print("[dim]  Skipping verification (--no-verify)")

    # ── Summary ─────────────────────────────────────────────────────
    elapsed = time.time() - start_time

    summary = Table(title="Pipeline Summary", show_header=True)
    summary.add_column("Metric", style="bold cyan")
    summary.add_column("Value", style="bold white")
    summary.add_row("Total Collected", str(len(all_streams)))
    summary.add_row("After Dedup", str(len(unique_streams)))
    summary.add_row("After Filter", str(len(filtered)))
    summary.add_row("Countries Found", str(len(grouped)))
    if verified_count is not None:
        summary.add_row("Verified Alive", f"{verified_count}/{len(filtered)}")
    summary.add_row("Time Elapsed", f"{elapsed:.1f}s")
    summary.add_row("Output Directory", output_dir)

    console.print()
    console.print(Panel(summary, border_style="green"))

    return {
        "total_collected": len(all_streams),
        "unique": len(unique_streams),
        "filtered": len(filtered),
        "countries": len(grouped),
        "verified": verified_count,
        "elapsed_seconds": round(elapsed, 1),
        "output_dir": output_dir,
    }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ALL-IN-ONE IPTV Engine — Playlist Aggregator & Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input", default="input",
        help="Directory containing local .m3u files (default: input)"
    )
    parser.add_argument(
        "--output", default="output",
        help="Output directory for generated playlists (default: output)"
    )
    parser.add_argument(
        "--no-verify", action="store_true",
        help="Skip stream health verification"
    )
    parser.add_argument(
        "--workers", type=int, default=25,
        help="Number of concurrent verification workers (default: 25)"
    )
    parser.add_argument(
        "--timeout", type=int, default=10,
        help="Verification timeout per stream in seconds (default: 10)"
    )

    args = parser.parse_args()

    try:
        result = asyncio.run(
            run_pipeline(
                input_dir=args.input,
                output_dir=args.output,
                verify=not args.no_verify,
                workers=args.workers,
                verify_timeout=args.timeout,
            )
        )
        if result.get("status") == "error":
            sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Pipeline interrupted by user.")
        sys.exit(130)
    except Exception as exc:
        console.print(f"[bold red]Pipeline failed: {exc}")
        logger.exception("Pipeline failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
