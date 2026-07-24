"""
Xtream Codes API parser & converter.
"""

from typing import List, Dict, Any


class XtreamParser:
    """Parser for Xtream Codes API stream objects and categories."""

    def __init__(self, host: str, username: str, password: str):
        self.host = host.rstrip('/')
        self.username = username
        self.password = password

    def convert_to_m3u_items(
        self,
        streams: List[Dict[str, Any]],
        categories: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Convert Xtream streams json list to standardized M3U items."""
        cat_map = {str(c.get("category_id")): c.get("category_name", "General") for c in categories}
        items = []

        for s in streams:
            stream_id = s.get("stream_id")
            name = s.get("name", "Unknown")
            cat_id = str(s.get("category_id", ""))
            group = cat_map.get(cat_id, "General")
            logo = s.get("stream_icon", "")
            ext = s.get("container_extension", "m3u8")

            url = f"{self.host}/live/{self.username}/{self.password}/{stream_id}.{ext}"

            items.append({
                "stream_id": stream_id,
                "name": name,
                "group": group,
                "url": url,
                "tvg_logo": logo,
            })

        return items
