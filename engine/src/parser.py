"""
M3U Parser — Parse M3U/M3U8 playlist content into structured channel data.
"""

import re

from .utils import setup_logging, normalize_channel_name, detect_country_from_group, sanitize_text, has_special_headers

logger = setup_logging("engine.parser")


class M3UParser:
    """Parse M3U playlist content into structured channel dictionaries."""

    def parse(self, content: str, source: str = "unknown") -> list[dict]:
        """Parse M3U content string into list of channel dicts."""
        channels = []
        lines = content.splitlines()

        current_extinf = None
        current_vlc_opts = []
        current_kodi_props = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("#EXTINF"):
                # Save previous channel if exists
                if current_extinf is not None:
                    # URL will be captured on next non-comment line
                    pass
                current_extinf = line
                current_vlc_opts = []
                current_kodi_props = []

            elif line.startswith("#EXTVLCOPT") or line.startswith("#EXTHTTP"):
                current_vlc_opts.append(line)

            elif line.startswith("#KODIPROP"):
                current_kodi_props.append(line)

            elif not line.startswith("#"):
                # This is a URL line
                if current_extinf is not None:
                    channel = self._parse_channel(
                        current_extinf, line, current_vlc_opts, current_kodi_props, source
                    )
                    if channel:
                        channels.append(channel)

                # Reset for next channel
                current_extinf = None
                current_vlc_opts = []
                current_kodi_props = []

        return channels

    def parse_all(self, sources: list[dict]) -> list[dict]:
        """Parse multiple playlist sources."""
        all_channels = []
        for source_data in sources:
            content = source_data.get("content", "")
            source = source_data.get("source", "unknown")
            if content:
                channels = self.parse(content, source)
                all_channels.extend(channels)
                logger.debug(f"Parsed {len(channels)} channels from {source}")
        return all_channels

    def _parse_channel(
        self, extinf: str, url: str, vlc_opts: list[str], kodi_props: list[str], source: str
    ) -> dict | None:
        """Parse a single channel from EXTINF + URL."""
        # Extract channel name
        name_match = re.search(r',(.*)$', extinf)
        name = sanitize_text(name_match.group(1).strip()) if name_match else "Unknown"

        # Extract TVG ID
        tvg_id = self._extract(extinf, r'tvg-id="([^"]*)"')

        # Extract TVG Name
        tvg_name = self._extract(extinf, r'tvg-name="([^"]*)"')

        # Extract TVG Country (country code)
        tvg_country = self._extract(extinf, r'tvg-country="([^"]*)"')

        # Extract TVG Logo
        tvg_logo = self._extract(extinf, r'tvg-logo="([^"]*)"')

        # Extract Group Title
        group_title = self._extract(extinf, r'group-title="([^"]*)"')

        # Determine country/group
        if tvg_country:
            group = detect_country_from_group(tvg_country)
        elif group_title:
            group = detect_country_from_group(group_title)
        else:
            group = "Uncategorized"

        # Build HTTP headers list (cookies, auth, etc.)
        http_headers = []
        for opt in vlc_opts:
            # Parse #EXTVLCOPT:http-header=Cookie: xxx
            header_match = re.search(r'http-header=(.+)', opt)
            if header_match:
                http_headers.append(header_match.group(1).strip())
            else:
                http_headers.append(opt)

        return {
            "name": name,
            "tvg_id": tvg_id or "",
            "tvg_name": tvg_name or "",
            "tvg_country": tvg_country or "",
            "tvg_logo": tvg_logo or "",
            "group": group,
            "group_title": group_title or "",
            "url": url.strip(),
            "extinf": extinf.strip(),
            "vlc_opts": vlc_opts,
            "kodi_props": kodi_props,
            "http_headers": http_headers,
            "source": source,
            "has_cookies": has_special_headers({
                "url": url,
                "vlc_opts": vlc_opts,
            }),
        }

    @staticmethod
    def _extract(text: str, pattern: str) -> str:
        """Extract a value from regex pattern."""
        match = re.search(pattern, text)
        return match.group(1).strip() if match else ""