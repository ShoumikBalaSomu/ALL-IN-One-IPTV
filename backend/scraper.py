import asyncio
import aiohttp
import re
import os
import glob
import json
import logging
from collections import defaultdict
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DATA_SOURCES = [
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
    "https://raw.githubusercontent.com/bugsfreeweb/Radio/refs/heads/main/radios/bdradios.json",
    "https://raw.githubusercontent.com/zilong7728/Collect-IPTV/refs/heads/main/best_sorted.m3u",
    "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8",
    "https://iptv-org.github.io/iptv/index.m3u",
    "https://raw.githubusercontent.com/ewchew/sports/refs/heads/main/liveeventsfilter.m3u8",
    "https://www.apsattv.com/localnow.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/tcl-playlist-generator/refs/heads/main/tcl.m3u8",
    "https://raw.githubusercontent.com/BuddyChewChew/lg-playlist-generator/refs/heads/main/lg_channels_us.m3u",
    "https://raw.githubusercontent.com/BuddyChewChew/xumo-playlist-generator/refs/heads/main/playlists/xumo_playlist.m3u",
    "https://raw.githubusercontent.com/Alplox/json-teles/refs/heads/main/channels.m3u",
    "https://romaxa55.github.io/world_ip_tv/output/index.m3u",
    "https://raw.githubusercontent.com/joaquinito2036-rgb/iptvfast/refs/heads/main/output/all.m3u"
]

def extract_channel_info(extinf):
    name_match = re.search(r',(.*)$', extinf)
    name = name_match.group(1).strip() if name_match else "Unknown"
    
    group = "Uncategorized"
    country_match = re.search(r'tvg-country="([^"]+)"', extinf)
    if country_match:
        group = country_match.group(1)
    else:
        group_match = re.search(r'group-title="([^"]+)"', extinf)
        if group_match:
            group = group_match.group(1)
            
    return name, group

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
        elif line.startswith("#EXTVLCOPT") or line.startswith("#EXTHTTP"):
            current_vlc.append(line)
        elif not line.startswith("#"):
            if current_extinf and line:
                name, group = extract_channel_info(current_extinf)
                channels.append({
                    "name": name,
                    "group": group,
                    "extinf": current_extinf,
                    "vlc_opts": current_vlc,
                    "url": line
                })
                current_extinf = None
                current_vlc = []
    return channels

def fold_and_write(channels, output_path):
    grouped = defaultdict(lambda: defaultdict(list))
    for c in channels:
        grouped[c["group"]][c["name"]].append(c)
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for group in sorted(grouped.keys()):
            for name in sorted(grouped[group].keys()):
                streams = grouped[group][name]
                primary = streams[0]
                f.write(primary["extinf"] + "\n")
                for stream in streams:
                    for opt in stream["vlc_opts"]:
                        f.write(opt + "\n")
                    f.write(stream["url"] + "\n")

async def check_host(session, host_url, timeout=5):
    try:
        async with session.get(host_url, timeout=timeout) as response:
            return 200 <= response.status < 400
    except Exception:
        return False

async def fetch_playlist(session, url):
    try:
        async with session.get(url, timeout=15) as response:
            if response.status == 200:
                logging.info(f"Fetched: {url}")
                return await response.text()
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
    return ""

async def main():
    os.makedirs("temp", exist_ok=True)
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    async with aiohttp.ClientSession() as session:
        logging.info("Step 1: Fetching M3U Playlists...")
        tasks = [fetch_playlist(session, url) for url in DATA_SOURCES]
        results = await asyncio.gather(*tasks)
        
        all_channels = []
        for res in results:
            if res:
                all_channels.extend(parse_m3u(res))
                
        for file in glob.glob("input/*.m3u") + glob.glob("input/*.m3u8"):
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    all_channels.extend(parse_m3u(f.read()))
            except Exception as e:
                logging.error(f"Error reading {file}: {e}")
                
        # Deduplicate exact URLs
        unique_channels_dict = {}
        for c in all_channels:
            if c["url"] not in unique_channels_dict:
                unique_channels_dict[c["url"]] = c
                
        unique_channels = list(unique_channels_dict.values())
        logging.info(f"Total unique URLs found: {len(unique_channels)}")
        
        # Write File 1: The Raw Combined List
        fold_and_write(unique_channels, "output/combined_by_country.m3u")
        logging.info("Generated output/combined_by_country.m3u")

        # Step 2: Health Checking
        logging.info("Step 2: Checking Host Health...")
        host_map = defaultdict(list)
        for c in unique_channels:
            parsed = urlparse(c["url"])
            host = f"{parsed.scheme}://{parsed.netloc}"
            host_map[host].append(c)
            
        alive_hosts = set()
        semaphore = asyncio.Semaphore(50)
        
        async def sem_check(host):
            async with semaphore:
                test_url = host_map[host][0]["url"]
                async with aiohttp.ClientSession() as inner_session:
                    if await check_host(inner_session, test_url):
                        alive_hosts.add(host)
                        
        check_tasks = [sem_check(host) for host in host_map.keys()]
        await asyncio.gather(*check_tasks)
        
        logging.info(f"Alive hosts: {len(alive_hosts)} out of {len(host_map)}")
        
        alive_channels = []
        for c in unique_channels:
            parsed = urlparse(c["url"])
            host = f"{parsed.scheme}://{parsed.netloc}"
            if host in alive_hosts:
                alive_channels.append(c)
                
        # Write File 2: The Checked Combined List
        fold_and_write(alive_channels, "output/checked_combined_by_country.m3u")
        logging.info("Generated output/checked_combined_by_country.m3u")

if __name__ == "__main__":
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
