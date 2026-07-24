# 📝 Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Machine Learning models for genre categorization.
- Native Apple TV app support (via Flutter).

## [2.0.0] - 2026-07-24
### Added
- **Major Rebuild:** The entire architecture has been rewritten for scalability and performance.
- Full asynchronous support for scrapers and validators utilizing `aiohttp` and `asyncio`.
- Implemented robust `FFprobe` based validator for deep stream inspection.
- Added comprehensive Docker support with multi-stage builds.
- New stunning UI/UX for all documentation files.
- GitHub Actions pipeline for automated daily playlist updates.

### Changed
- Improved regex parsing for varied M3U formats.
- Reduced memory footprint of the deduplication engine by 40%.
- Switched to Python 3.12 as the minimum required version.

### Removed
- Legacy synchronous `requests` based scrapers.

## [1.0.0] - 2024-05-10
### Added
- Initial release.
- Basic scraping capabilities for 5 major open IPTV sources.
- Simple M3U merging tool.