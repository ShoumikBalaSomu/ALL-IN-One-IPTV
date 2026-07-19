import asyncio
import aiohttp
import re
import os
import glob
from collections import defaultdict
import logging
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# DATA SOURCES (M3U PLAYLISTS TO AGGREGATE)
DATA_SOURCES = [
    "https://raw.githubusercontent.com/sm-monirulislam/SM-Live-TV/refs/heads/main/Combined_Live_TV.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/SM-Movie-Hup-Auto-Update/refs/heads/main/Movie_Combined.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/AynaOTT-auto-update-playlist/refs/heads/main/AynaOTT.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/Toffee-Auto-Update-Playlist/refs/heads/main/toffee_playlist.m3u",
    "https://private-zone-by-xfireflix.pages.dev/BDIX1.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/BDxTV/refs/heads/main/playlist_s.m3u",
    "https://raw.githubusercontent.com/Mrbotrx/bdxi_tv/main/kbtvpro.m3u8",
    "https://movie-playlist-byxfireflix.pages.dev/movie-playlist.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/Movie-Playlist-Auto-update/refs/heads/main/Mix_Movies.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/main/playlist.m3u",
    "https://raw.githubusercontent.com/ashik4u/mrgify-clean/refs/heads/main/playlist.m3u",
    "https://raw.githubusercontent.com/tahsinulmohsin/jagobd-m3u8-scraper/master/playlist.m3u8",
    "https://raw.githubusercontent.com/ashik4u/iptv-m3u-bot/refs/heads/main/output/all.m3u",
    "https://raw.githubusercontent.com/opensourceflix/OpenSourceFlix/refs/heads/main/iptv.m3u8",
    "https://raw.githubusercontent.com/opensourceflix/OpenSourceFlix/main/papaos.m3u8",
    "https://raw.githubusercontent.com/alberttartas/Pirataflix/refs/heads/main/input_auto/TV/iptv_org_br.m3u",
    "https://raw.githubusercontent.com/alberttartas/Pirataflix/refs/heads/main/iptv_playlists/vod_grouped.m3u",
    "http://202.70.146.135:8000/playlist.m3u",
    "https://la.drmlive.net/tp/playlist",
    "https://raw.githubusercontent.com/abusaeeidx/CricHd-playlists-Auto-Update-permanent/refs/heads/main/ALL.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/CricHD-Auto-Update-Playlist/refs/heads/main/crichd.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/FanCode-Auto-Update-Playlist/refs/heads/main/fancode_bd.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/FanCode-Auto-Update-Playlist/refs/heads/main/fancode_in.m3u",
    "https://raw.githubusercontent.com/sm-monirulislam/Tapmad_Auto_Update_Playlist/refs/heads/main/Tapmad_sm.m3u",
    "https://iptv-org.github.io/iptv/index.m3u"
]

class Channel:
    def __init__(self, extinf, vlc_opts, url):
        self.extinf = extinf
        self.vlc_opts = vlc_opts
        self.url = url
        
        # Extract channel name
        match = re.search(r',(.*)$', extinf)
        self.name = match.group(1).strip() if match else "Unknown"
        
        # Extract group title / country
        group_match = re.search(r'group-title="([^"]+)"', extinf)
        self.group = group_match.group(1) if group_match else "Uncategorized"
        
        country_match = re.search(r'tvg-country="([^"]+)"', extinf)
        if country_match:
            self.group = country_match.group(1)
            
    def __hash__(self):
        return hash(self.url)
        
    def __eq__(self, other):
        return self.url == other.url

async def fetch_playlist(session, url):
    try:
        async with session.get(url, timeout=15) as response:
            if response.status == 200:
                logging.info(f"Successfully fetched: {url}")
                return await response.text()
            else:
                logging.warning(f"Failed to fetch {url}: Status {response.status}")
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
    return ""

def parse_m3u(content):
    channels = []
    lines = content.splitlines()
    
    current_extinf = None
    current_vlc = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("#EXTINF"):
            current_extinf = line
            current_vlc = []
        elif line.startswith("#EXTVLCOPT"):
            current_vlc.append(line)
        elif not line.startswith("#"):
            if current_extinf and line:
                channels.append(Channel(current_extinf, current_vlc, line))
                current_extinf = None
                current_vlc = []
    return channels

async def check_stream(session, channel, host_status_cache):
    parsed = urlparse(channel.url)
    host = parsed.netloc
    
    if host in host_status_cache:
        if host_status_cache[host]:
            return True
            
    try:
        # Some servers block HEAD requests, use GET with stream=True or just a quick GET and close
        async with session.get(channel.url, timeout=5) as response:
            is_alive = 200 <= response.status < 300
            if is_alive:
                host_status_cache[host] = True
            return is_alive
    except Exception:
        return False

async def main():
    async with aiohttp.ClientSession() as session:
        logging.info("Fetching playlists...")
        tasks = [fetch_playlist(session, url) for url in DATA_SOURCES]
        results = await asyncio.gather(*tasks)
        
        all_channels = []
        for res in results:
            if res:
                all_channels.extend(parse_m3u(res))
                
        # Read from input folder if exists
        if os.path.exists("input"):
            for file in glob.glob("input/*.m3u") + glob.glob("input/*.m3u8"):
                try:
                    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                        all_channels.extend(parse_m3u(f.read()))
                except Exception as e:
                    logging.error(f"Error reading {file}: {e}")
                    
        # Deduplicate
        unique_channels_dict = {c.url: c for c in all_channels}
        unique_channels = list(unique_channels_dict.values())
        logging.info(f"Total unique channels found: {len(unique_channels)}")
        
        # Group by country/group
        grouped_channels = defaultdict(list)
        for c in unique_channels:
            grouped_channels[c.group].append(c)
            
        os.makedirs("output", exist_ok=True)
        
        # Write Combined by Country
        with open("output/Combined_by_Country.m3u", "w", encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for group in sorted(grouped_channels.keys()):
                for c in sorted(grouped_channels[group], key=lambda x: x.name):
                    f.write(c.extinf + "\n")
                    for opt in c.vlc_opts:
                        f.write(opt + "\n")
                    f.write(c.url + "\n")
                    
        logging.info("Wrote Combined_by_Country.m3u. Starting health checks...")
        
        # Health Check
        # Limit concurrency to 50 to avoid maxing out connections or getting banned
        semaphore = asyncio.Semaphore(50)
        host_status_cache = {}
        
        async def sem_check(channel):
            async with semaphore:
                is_alive = await check_stream(session, channel, host_status_cache)
                return channel if is_alive else None
                
        check_tasks = [sem_check(c) for c in unique_channels]
        checked_results = await asyncio.gather(*check_tasks)
        
        alive_channels = [c for c in checked_results if c]
        logging.info(f"Alive channels: {len(alive_channels)}")
        
        grouped_alive = defaultdict(list)
        for c in alive_channels:
            grouped_alive[c.group].append(c)
            
        with open("output/Checked_Combined_by_Country.m3u", "w", encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for group in sorted(grouped_alive.keys()):
                for c in sorted(grouped_alive[group], key=lambda x: x.name):
                    f.write(c.extinf + "\n")
                    for opt in c.vlc_opts:
                        f.write(opt + "\n")
                    f.write(c.url + "\n")
                    
        logging.info("Done generating Checked_Combined_by_Country.m3u")

if __name__ == "__main__":
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
