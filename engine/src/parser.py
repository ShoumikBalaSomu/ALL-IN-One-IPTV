from dataclasses import dataclass, field
from typing import List, Dict, Optional
import re
from .exceptions import ParserError

@dataclass
class Stream:
    url: str
    name: str = ""
    tvg_id: str = ""
    tvg_name: str = ""
    tvg_logo: str = ""
    group_title: str = ""
    tvg_language: str = ""
    tvg_country: str = ""
    quality: str = "Unknown"
    qrs_score: float = 0.0
    fallbacks: List[str] = field(default_factory=list)
    has_cookies: bool = False
    vlc_opts: Dict[str, str] = field(default_factory=dict)
    
    def __hash__(self):
        return hash(self.url)
        
    def __eq__(self, other):
        if not isinstance(other, Stream):
            return False
        return self.url == other.url

class M3UParser:
    @staticmethod
    def parse(content: str) -> List[Stream]:
        streams = []
        lines = content.strip().splitlines()
        current_stream = Stream(url="")
        for line in lines:
            line = line.strip()
            if line.startswith("#EXTINF:"):
                current_stream = Stream(url="")
                if "," in line:
                    current_stream.name = line.split(",", 1)[1].strip()
                tvg_id = re.search(r'tvg-id="([^"]+)"', line)
                if tvg_id: current_stream.tvg_id = tvg_id.group(1)
                tvg_name = re.search(r'tvg-name="([^"]+)"', line)
                if tvg_name: current_stream.tvg_name = tvg_name.group(1)
                tvg_logo = re.search(r'tvg-logo="([^"]+)"', line)
                if tvg_logo: current_stream.tvg_logo = tvg_logo.group(1)
                group_title = re.search(r'group-title="([^"]+)"', line)
                if group_title: current_stream.group_title = group_title.group(1)
            elif line.startswith("#EXTVLCOPT:"):
                key_val = line[11:].split("=", 1)
                if len(key_val) == 2:
                    current_stream.vlc_opts[key_val[0]] = key_val[1]
            elif not line.startswith("#") and line:
                current_stream.url = line
                streams.append(current_stream)
                current_stream = Stream(url="")
        return streams

    @staticmethod
    def generate(streams: List[Stream]) -> str:
        lines = ["#EXTM3U"]
        for s in streams:
            extinf = f'#EXTINF:-1 tvg-id="{s.tvg_id}" tvg-name="{s.tvg_name}" tvg-logo="{s.tvg_logo}" group-title="{s.group_title}",{s.name}'
            lines.append(extinf)
            for k, v in s.vlc_opts.items():
                lines.append(f'#EXTVLCOPT:{k}={v}')
            for fb in s.fallbacks:
                lines.append(f'#EXTVLCOPT:fallback={fb}')
            lines.append(s.url)
        return "\n".join(lines)
