# ⚙️ Python Engine Technical Manual

Welcome to the core brain of the **ALL-IN-One IPTV** ecosystem. This Python engine handles the heavy lifting: harvesting, verifying, deduping, and healing streams at blistering speeds.

## 🐍 Prerequisites
- **Python 3.12+**
- Packages: `aiohttp`, `uvloop`, `rich`, `structlog`

## 🚀 CLI Flags Documentation

The engine is primarily invoked via `cli.py`.

```bash
python engine/cli.py [OPTIONS]
```

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--input` | String | *Required* | Path to the raw, unverified `.m3u` file. |
| `--output` | String | `verified.m3u` | Output path for the clean playlist. |
| `--workers` | Integer | `500` | Number of concurrent `asyncio` workers. Higher = faster, but needs more network bandwidth. |
| `--no-verify` | Boolean | `False` | Skips HTTP HEAD/GET verification (useful for rapid deduping only). |
| `--ai-heal` | Boolean | `False` | Activates the AI Quantum Healer to attempt repair of broken links. |
| `--timeout` | Float | `1.5` | Max timeout in seconds for a stream to respond before failing. |
| `--log-level` | String | `INFO` | Set to `DEBUG`, `INFO`, `WARNING`, or `ERROR`. |

### Examples

**Standard Verification:**
```bash
python engine/cli.py --input raw.m3u --output verified.m3u --workers 500
```

**Aggressive Verification & Healing (Production):**
```bash
python engine/cli.py --input master_raw.m3u --output master_clean.m3u --workers 1000 --ai-heal --timeout 2.0
```

---

## 📚 API Reference

If you are importing the engine as a module into your own Python scripts, here are the core components:

### 1. `collector`
Handles reading, parsing, and normalizing M3U files into Python dataclasses.
```python
from engine.collector import M3UParser

parser = M3UParser("raw.m3u")
streams = parser.parse() # Returns List[StreamData]
```

### 2. `verifier`
The `asyncio` loop manager and HTTP client pool.
```python
from engine.verifier import AsyncSentinel

sentinel = AsyncSentinel(workers=500, timeout=1.5)
clean_streams = await sentinel.verify_all(streams)
```

### 3. `ai_healer`
The heuristic mutation engine.
```python
from engine.ai_healer import QuantumHealer

healer = QuantumHealer()
repaired_stream = await healer.attempt_repair(broken_stream)
```

### 4. `deduplicator`
Fuzzy logic matching for channel names to remove redundant links.
```python
from engine.deduplicator import FuzzyDeduplicator

deduper = FuzzyDeduplicator(threshold=0.85)
unique_streams = deduper.process(clean_streams)
```

### 5. `grouper` & `exporter`
Categorizes streams by `#EXTGRP` or `tvg-group` and exports the final M3U.
```python
from engine.exporter import M3UExporter

exporter = M3UExporter(output_path="verified.m3u")
exporter.write(unique_streams)
```

---
> [!TIP]
> **Performance Tuning:** If you encounter `Too many open files` errors, increase your OS file descriptor limit using `ulimit -n 65535` before running high-worker tasks.
