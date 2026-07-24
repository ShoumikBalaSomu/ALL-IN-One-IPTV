from typing import List
from .parser import Stream

class XtreamParser:
    @staticmethod
    def parse_api_response(data: List[dict]) -> List[Stream]:
        streams = []
        for item in data:
            s = Stream(
                url=item.get("url", ""),
                name=item.get("name", ""),
                tvg_logo=item.get("stream_icon", ""),
                tvg_id=str(item.get("epg_channel_id", "")),
                group_title=item.get("category_name", "")
            )
            streams.append(s)
        return streams
