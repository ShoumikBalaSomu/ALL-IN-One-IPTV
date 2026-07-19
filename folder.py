import json
import os
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fold_and_write(channels, output_path):
    # Group by Country -> Channel Name
    grouped = defaultdict(lambda: defaultdict(list))
    for c in channels:
        grouped[c["group"]][c["name"]].append(c)
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for group in sorted(grouped.keys()):
            for name in sorted(grouped[group].keys()):
                streams = grouped[group][name]
                # Write the first #EXTINF as the primary
                primary = streams[0]
                f.write(primary["extinf"] + "\n")
                
                # Write all URLs under this single #EXTINF for fallback streaming
                for stream in streams:
                    for opt in stream["vlc_opts"]:
                        f.write(opt + "\n")
                    f.write(stream["url"] + "\n")

def main():
    if not os.path.exists("temp/scraped.json"):
        logging.error("temp/scraped.json not found. Run scraper.py first.")
        return
        
    with open("temp/scraped.json", "r", encoding="utf-8") as f:
        channels = json.load(f)
        
    fold_and_write(channels, "output/combined_by_country.m3u")
    logging.info(f"Folded {len(channels)} URLs into combined_by_country.m3u")

if __name__ == "__main__":
    main()
