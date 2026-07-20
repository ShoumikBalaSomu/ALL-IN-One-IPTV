import asyncio
import aiohttp
import requests
import re
import os
import time

PLAYLISTS = [
    "https://raw.githubusercontent.com/sm-monirulislam/SM-Live-TV/refs/heads/main/Combined_Live_TV.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/SM-Movie-Hup-Auto-Update/refs/heads/main/Movie_Combined.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/AynaOTT-auto-update-playlist/refs/heads/main/AynaOTT.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/Toffee-Auto-Update-Playlist/refs/heads/main/toffee_playlist.m3u",
    "https://private-zone-by-xfireflix.pages.dev/BDIX1.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/BDxTV/refs/heads/main/playlist_s.m3u",
    "https://movie-playlist-byxfireflix.pages.dev/movie-playlist.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/Movie-Playlist-Auto-update/refs/heads/main/Mix_Movies.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/main/playlist.m3u",
    "https://raw.githubusercontent.com/ashik4u/mrgify-clean/refs/heads/main/playlist.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/Toffee-playlist/refs/heads/main/ott_navigator.m3u",
    "https://raw.githubusercontent.com/Mrbotrx/bdxi_tv/main/kbtvpro.m3u8",
    "https://raw.githubusercontent.com/johirxofficial/aynaott-auto-update-playlist/refs/heads/main/AynaOTT.m3u",
    "https://raw.githubusercontent.com/johirxofficial/Toffee-Auto-Playlist/refs/heads/main/toffee_playlist.m3u",
    "https://raw.githubusercontent.com/tahsinulmohsin/jagobd-m3u8-scraper/master/playlist.m3u8",
    "https://raw.githubusercontent.com/ashik4u/iptv-m3u-bot/refs/heads/main/output/all.m3u",
    "https://raw.githubusercontent.com/opensourceflix/OpenSourceFlix/refs/heads/main/iptv.m3u8",
    "https://raw.githubusercontent.com/etcvai/ExtenderMax/refs/heads/main/iptv.m3u8",
    "https://raw.githubusercontent.com/opensourceflix/OpenSourceFlix/main/papaos.m3u8",
    "https://go.skym3u.top/fyeo.m3u",
    "https://raw.githubusercontent.com/sanjoykb/-KB-TV-Playlist/refs/heads/main/Github%20Auto%20Update%20Channel.m3u",
    "https://raw.githubusercontent.com/alberttartas/Pirataflix/refs/heads/main/input_auto/TV/iptv_org_br.m3u",
    "https://raw.githubusercontent.com/alberttartas/Pirataflix/refs/heads/main/iptv_playlists/vod_grouped.m3u",
    "http://202.70.146.135:8000/playlist.m3u",
    "https://iptvidn-playlist.vercel.app/playlist.m3u8",
    "https://raw.githubusercontent.com/abusaeeidx/IPTV-Scraper-Zilla/main/combined-playlist.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/Yupptv-Playlist/refs/heads/main/playlist.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/Yupptv-Playlist/refs/heads/main/playlist_v2.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/CricHd-playlists-Auto-Update-permanent/refs/heads/main/ALL.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/CricHD-Scraper-V2/main/playlist.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/IP-Stream/refs/heads/main/playlist.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/FanCode-Auto-Update-Playlist/refs/heads/main/fancode_bd.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/FanCode-Auto-Update-Playlist/refs/heads/main/fancode_in.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/Tapmad_Auto_Update_Playlist/refs/heads/main/Tapmad_sm.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/CricHD-Auto-Update-Playlist/refs/heads/main/crichd.m3u",
    "https://raw.githubusercontent.com/Love4vn/Love4xt/refs/heads/1/output.m3u",
    "https://raw.githubusercontent.com/Love4vn/Love4xt/refs/heads/1/output_clean.m3u",
    "https://raw.githubusercontent.com/Love4vn/Match_Stream/refs/heads/1/Football_match_live.m3u",
    "https://raw.githubusercontent.com/Love4vn/Match_Stream/refs/heads/1/Mac_playlist.m3u",
    "https://raw.githubusercontent.com/Love4vn/Match_Stream/refs/heads/1/live_schedule_Optimize.m3u",
    "https://raw.githubusercontent.com/Love4vn/Test/refs/heads/main/IPTV.m3u",
    "https://raw.githubusercontent.com/Love4vn/Stalker2M3U-public/refs/heads/main/Mac_playlist.m3u",
    "https://raw.githubusercontent.com/Love4vn/Stalker2M3U-public/refs/heads/main/Football_match_live.m3u",
    "https://raw.githubusercontent.com/Love4vn/Stalker2M3U-public/refs/heads/main/live_schedule_Optimize.m3u",
    "https://raw.githubusercontent.com/Mrbotrx/Tvbox_KB/main/kb_tv.m3u",
    "https://raw.githubusercontent.com/Mrbotrx/All-FREE-TV/main/combined_playlist.m3u",
    "https://raw.githubusercontent.com/johirxofficial/otv-auto-updated-playlist/main/otv.m3u",
    "https://raw.githubusercontent.com/imShakil/tvlink/refs/heads/main/all.m3u",
    "https://link.dekhoprime.live/m3u/bd/1782385148-ant-ferret-dingo.m3u",
    "https://link.dekhoprime.live/m3u/world/1782385148-moose-wolf-goose.m3u",
    "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/jtv.m3u",
    "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/jstar.m3u",
    "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/jcinema.m3u",
    "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/amzusa.m3u",
    "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/dishtv.m3u",
    "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/lgtv.m3u",
    "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/suntv.m3u",
    "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/z5.m3u",
    "https://raw.githubusercontent.com/judy-gotv/iptv/refs/heads/main/combined-playlist.m3u",
    "https://la.drmlive.net/tp/playlist",
    "https://raw.githubusercontent.com/bugsfreeweb/LiveTVCollector/refs/heads/main/LiveTV/Bangladesh/LiveTV.m3u",
    "https://raw.githubusercontent.com/zilong7728/Collect-IPTV/refs/heads/main/best_sorted.m3u",
    "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8",
    "https://iptv-org.github.io/iptv/index.m3u",
    "https://raw.githubusercontent.com/ewchew/sports/main/liveeventsfilter.m3u8",
    "https://www.apsattv.com/localnow.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/tcl-playlist-generator/refs/heads/main/tcl.m3u8",
    "https://raw.githubusercontent.com/BuddyChewChew/lg-playlist-generator/refs/heads/main/lg_channels_us.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/xumo-playlist-generator/refs/heads/main/playlists/xumo_playlist.m3u",
    "https://raw.githubusercontent.com/Alplox/json-teles/refs/heads/main/channels.m3u",
    "https://romaxa55.github.io/world_ip_tv/output/index.m3u",
    "https://raw.githubusercontent.com/joaquinito2036-rgb/iptvfast/refs/heads/main/output/all.m3u"
]

class Channel:
    def __init__(self, extinf, url, http_headers=None):
        self.extinf = extinf.strip()
        self.url = url.strip()
        self.http_headers = http_headers or []
        
        # Extract metadata
        self.title = self._extract(r',([^,]*)$')
        self.group = self._extract(r'group-title="([^"]*)"')
        if not self.group:
            self.group = "Uncategorized"
        
        # Normalize title for folding
        self.norm_title = re.sub(r'[^a-zA-Z0-9]', '', self.title.lower()) if self.title else ""
        
        # Check if URL has cookies/tokens
        self.has_cookies = "?" in self.url or "cookie" in self.url.lower() or "token" in self.url.lower()

    def _extract(self, pattern):
        match = re.search(pattern, self.extinf)
        return match.group(1).strip() if match else ""

    def __str__(self):
        headers_str = "\n".join(self.http_headers)
        if headers_str:
            return f"{self.extinf}\n{headers_str}\n{self.url}"
        return f"{self.extinf}\n{self.url}"

def fetch_playlists():
    channels = []
    print("Fetching playlists...")
    for url in PLAYLISTS:
        try:
            print(f"Fetching {url}")
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                lines = resp.text.splitlines()
                current_extinf = None
                current_headers = []
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("#EXTINF"):
                        current_extinf = line
                        current_headers = []
                    elif line.startswith("#EXTVLCOPT") or line.startswith("#KODIPROP"):
                        current_headers.append(line)
                    elif not line.startswith("#"):
                        if current_extinf:
                            channels.append(Channel(current_extinf, line, current_headers))
                        current_extinf = None
                        current_headers = []
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
    return channels

def deduplicate_and_fold(channels):
    print(f"Total parsed channels: {len(channels)}")
    unique_urls = set()
    deduped = []
    
    # Simple folding dictionary
    folded = {}
    
    for ch in channels:
        if ch.url in unique_urls and not ch.has_cookies:
            continue
        unique_urls.add(ch.url)
        
        # Folder by normalized title + group
        key = f"{ch.group}_{ch.norm_title}"
        if key not in folded:
            folded[key] = ch
            deduped.append(ch)
        else:
            # If it has cookies, keep it anyway
            if ch.has_cookies:
                deduped.append(ch)

    print(f"Channels after deduplication and folding: {len(deduped)}")
    return deduped

async def check_url(session, ch):
    try:
        async with session.head(ch.url, timeout=5, allow_redirects=True) as response:
            return ch, response.status < 400
    except:
        return ch, False

async def validate_channels(channels):
    print("Validating channels asynchronously... This might take a few minutes.")
    valid_channels = []
    
    # Due to potentially huge number of channels (e.g. 50k+), limit concurrency
    connector = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [check_url(session, ch) for ch in channels]
        for idx, coro in enumerate(asyncio.as_completed(tasks)):
            ch, is_valid = await coro
            if is_valid:
                valid_channels.append(ch)
            if idx % 1000 == 0 and idx > 0:
                print(f"Checked {idx}/{len(channels)}")
                
    print(f"Valid channels: {len(valid_channels)}")
    return valid_channels

def export_m3u(channels, filename):
    # Group by country (which we map to 'group' property for now)
    channels.sort(key=lambda x: (x.group, x.title))
    
    os.makedirs("output", exist_ok=True)
    filepath = os.path.join("output", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in channels:
            f.write(str(ch) + "\n")
    print(f"Exported to {filepath}")

def main():
    channels = fetch_playlists()
    deduped = deduplicate_and_fold(channels)
    
    # Export un-checked combined
    export_m3u(deduped, "combined_by_country.m3u")
    
    # Validate and export checked
    valid_channels = asyncio.run(validate_channels(deduped))
    export_m3u(valid_channels, "checked_combined_by_country.m3u")

if __name__ == "__main__":
    main()
