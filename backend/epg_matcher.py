import re
try:
    from thefuzz import process, fuzz
except ImportError:
    # Fallback if thefuzz is not installed
    import difflib

class EPGMatcher:
    def __init__(self, master_epg_list):
        """
        master_epg_list: A list of dicts from your XMLTV file containing verified
        {'tvg_id': 'bbc_one', 'name': 'BBC One', 'logo': 'url'}
        """
        self.master_epg_list = master_epg_list
        self.master_names = [epg['name'] for epg in master_epg_list]

    def _clean_channel_name(self, raw_name):
        # Strip common M3U clutter
        clutter_tags = [
            r'\[HD\]', r'\[FHD\]', r'\[SD\]', r'\[4K\]', r'\[RAW\]',
            r'\(UK\)', r'\(US\)', r'1080p', r'720p', r'HEVC', r'H265'
        ]
        
        cleaned = raw_name
        for tag in clutter_tags:
            cleaned = re.sub(tag, '', cleaned, flags=re.IGNORECASE)
            
        # Remove multiple spaces and strip
        return re.sub(r'\s+', ' ', cleaned).strip()

    def find_best_match(self, raw_channel_name, threshold=85):
        cleaned_name = self._clean_channel_name(raw_channel_name)
        
        try:
            # Using thefuzz (Levenshtein Distance)
            match, score = process.extractOne(cleaned_name, self.master_names, scorer=fuzz.token_sort_ratio)
            if score >= threshold:
                return next(epg for epg in self.master_epg_list if epg['name'] == match)
        except NameError:
            # Fallback using difflib
            matches = difflib.get_close_matches(cleaned_name, self.master_names, n=1, cutoff=threshold/100.0)
            if matches:
                return next(epg for epg in self.master_epg_list if epg['name'] == matches[0])
                
        return None

if __name__ == "__main__":
    # Example Usage
    mock_epg = [
        {'tvg_id': 'sky_sports_main', 'name': 'Sky Sports Main Event', 'logo': 'http://logo/sky.png'}
    ]
    matcher = EPGMatcher(mock_epg)
    
    raw_m3u_name = "Sky Sports Main Event [FHD] 1080p (UK)"
    result = matcher.find_best_match(raw_m3u_name)
    
    print(f"Raw: {raw_m3u_name} -> Matched: {result}")
