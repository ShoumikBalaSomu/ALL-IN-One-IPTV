"""
Torrent & Acestream P2P link bridge.
"""

import re
from typing import Optional


class TorrentStreamBridge:
    """Bridge for parsing and transforming Acestream and Torrent magnet links to HTTP proxy URLs."""

    def __init__(self, local_proxy_host: str = "127.0.0.1", local_proxy_port: int = 8080):
        self.local_proxy_host = local_proxy_host
        self.local_proxy_port = local_proxy_port

    def is_p2p_url(self, url: str) -> bool:
        """Check if URL is acestream or magnet link."""
        if not url:
            return False
        return url.startswith("acestream://") or url.startswith("magnet:") or ".torrent" in url

    def extract_infohash(self, url: str) -> Optional[str]:
        """Extract infohash or PID from acestream / magnet link."""
        if url.startswith("acestream://"):
            return url.replace("acestream://", "").strip()
        match = re.search(r"xt=urn:btih:([a-fA-F0-9]{40}|[a-zA-Z2-7]{32})", url)
        if match:
            return match.group(1)
        return None

    def transform_to_http_proxy(self, url: str) -> str:
        """Transform P2P link to HTTP local proxy endpoint."""
        infohash = self.extract_infohash(url)
        if infohash:
            return f"http://{self.local_proxy_host}:{self.local_proxy_port}/p2p/{infohash}"
        return url
