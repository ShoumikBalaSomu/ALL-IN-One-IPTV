# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-07-24

### Added
- **AI Quantum Stream Healer**: Implemented advanced heuristic scoring and token mutation for broken streams.
- **Glassmorphism UI**: Complete visual overhaul of the Flutter and Web clients using modern glassmorphism design principles.
- **500-Worker Verifier**: Upgraded the Python engine's concurrency limit, drastically improving verification speed.
- **Multi-view Grid**: Natively integrated multi-view channel grid in the Web Player and Flutter App.
- **Xtream Emulation**: Full emulation of the Xtream Codes API via the Ktor Gateway.
- **IPFS Resolver**: Experimental support for resolving P2P playlists via IPFS.

### Changed
- Migrated engine from standard `asyncio` loop to `uvloop` for 2x throughput.
- Fallback generation now utilizes `#EXTVLCOPT:fallback` for native VLC/mpv compatibility.

### Fixed
- Resolved memory leak in `aiohttp` client session pooling during extended 1M+ link verifications.

## [2.0.0] - 2025-11-15

### Added
- Multi-platform monorepo architecture (Flutter + Kotlin + Python).
- Initial release of Kotlin Compose Android TV app.
- Advanced fuzzy deduplicator using string distance metrics.

### Changed
- **Breaking**: Restructured entire repository layout to separate `engine`, `api`, and `clients`.

## [1.5.0] - 2025-06-10

### Added
- React-based Web Player with HLS.js integration.
- Automated EPG (Electronic Program Guide) injection.

### Fixed
- Fixed regex parsing errors for malformed EXTM3U tags.

## [1.0.0] - 2024-12-01

### Added
- Initial release of the Python M3U Verifier.
- Basic threaded worker pool.
- Simple M3U output generation.