"""
Torrent & P2P Stream Bridge Helper.
Parses acestream://, magnet:?, and P2P infohashes into local proxy HTTP URLs for zero-buffering playback.
"""

from urllib.parse import parse_qs, urlparse

class TorrentStreamBridge:
    """Transforms P2P / Acestream / Magnet URIs to HTTP proxy endpoints."""

    def __init__(self, local_proxy_port: int = 8080):
        self.local_proxy_port = local_proxy_port

    def is_p2p_url(self, url: str) -> bool:
        """Check if URL is a P2P / Acestream / Magnet stream."""
        return url.startswith("acestream://") or url.startswith("magnet:") or ".torrent" in url

    def extract_infohash(self, url: str) -> str | None:
        """Extract 40-character hex infohash or Acestream ID."""
        if url.startswith("acestream://"):
            return url.replace("acestream://", "").strip()

        if url.startswith("magnet:"):
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            xt_list = params.get('xt', [])
            for xt in xt_list:
                if 'btih:' in xt:
                    return xt.split('btih:')[-1].split('&')[0]

        return None

    def transform_to_http_proxy(self, url: str) -> str:
        """Transform a P2P URL into a local HTTP proxy relay URL."""
        if not self.is_p2p_url(url):
            return url

        infohash = self.extract_infohash(url)
        if infohash:
            return f"http://127.0.0.1:{self.local_proxy_port}/p2p/{infohash}"

        return url
