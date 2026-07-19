import asyncio
import aiohttp
import json
import os
from urllib.parse import urlparse
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def check_host(session, host_url, timeout=5):
    try:
        # Check using a quick GET request (HEAD is blocked by many servers)
        async with session.get(host_url, timeout=timeout) as response:
            return 200 <= response.status < 400
    except Exception:
        return False

async def main():
    if not os.path.exists("temp/scraped.json"):
        logging.error("temp/scraped.json not found. Run scraper.py first.")
        return
        
    with open("temp/scraped.json", "r", encoding="utf-8") as f:
        channels = json.load(f)
        
    # Group channels by base host to minimize checks
    host_map = defaultdict(list)
    for c in channels:
        parsed = urlparse(c["url"])
        host = f"{parsed.scheme}://{parsed.netloc}"
        host_map[host].append(c)
        
    logging.info(f"Total unique hosts to check: {len(host_map)}")
    
    alive_hosts = set()
    semaphore = asyncio.Semaphore(50)
    
    async def sem_check(host):
        async with semaphore:
            # We pick the first channel URL to test instead of just the base host, 
            # because some bases don't reply at root. 
            test_url = host_map[host][0]["url"]
            async with aiohttp.ClientSession() as session:
                is_alive = await check_host(session, test_url)
                if is_alive:
                    alive_hosts.add(host)
                    
    tasks = [sem_check(host) for host in host_map.keys()]
    await asyncio.gather(*tasks)
    
    logging.info(f"Alive hosts: {len(alive_hosts)} out of {len(host_map)}")
    
    alive_channels = []
    for c in channels:
        parsed = urlparse(c["url"])
        host = f"{parsed.scheme}://{parsed.netloc}"
        if host in alive_hosts:
            alive_channels.append(c)
            
    # Fold and write alive channels
    grouped = defaultdict(lambda: defaultdict(list))
    for c in alive_channels:
        grouped[c["group"]][c["name"]].append(c)
        
    os.makedirs("output", exist_ok=True)
    with open("output/checked_combined_by_country.m3u", "w", encoding="utf-8") as f:
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
                    
    logging.info(f"Folded {len(alive_channels)} alive URLs into checked_combined_by_country.m3u")

if __name__ == "__main__":
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
