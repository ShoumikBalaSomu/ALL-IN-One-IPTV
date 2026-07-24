"""
IPFS Gateway Publisher & resolver.
"""

from typing import List


class IPFSPublisher:
    """Publishes and formats IPFS URLs across public gateways."""

    DEFAULT_GATEWAYS = [
        "https://ipfs.io/ipfs/",
        "https://gateway.pinata.cloud/ipfs/",
        "https://dweb.link/ipfs/",
        "https://cloudflare-ipfs.com/ipfs/",
    ]

    def __init__(self, primary_gateway: str = "https://ipfs.io/ipfs/"):
        self.primary_gateway = primary_gateway.rstrip('/') + '/'

    def format_ipfs_url(self, cid: str) -> str:
        """Format CID into gateway URL."""
        return f"{self.primary_gateway}{cid}"

    def get_all_gateway_urls(self, cid: str) -> List[str]:
        """Get fallback URLs across public IPFS gateways."""
        return [f"{gw.rstrip('/')}/{cid}" for gw in self.DEFAULT_GATEWAYS]
