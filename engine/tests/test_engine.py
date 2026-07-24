"""
Tests for the IPTV Engine.
"""

import unittest
import sys
import os
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from engine.src.utils import (
    normalize_channel_name,
    url_to_host,
    detect_country_from_group,
    has_special_headers,
    sanitize_text,
)
from engine.src.parser import M3UParser, Stream
from engine.src.encryption import encrypt_playlist, decrypt_playlist, generate_key
from engine.src.epg_fetcher import EPGFetcher
from engine.src.xtream_parser import XtreamParser
from engine.src.torrent_bridge import TorrentStreamBridge
from engine.src.search_engine import ChannelSearchEngine
from engine.src.content_filter import ContentFilter
from engine.src.quality_classifier import StreamQualityClassifier
from engine.src.ipfs_publisher import IPFSPublisher
from engine.src.ai_healer import AIStreamHealer


class TestUtils(unittest.TestCase):
    """Test utility functions."""

    def test_normalize_channel_name(self):
        self.assertEqual(normalize_channel_name("Star Sports [HD] 1080p"), "star sports")
        self.assertEqual(normalize_channel_name("BBC News (UK) [FHD]"), "bbc news")
        self.assertEqual(normalize_channel_name("  Geo News HD  "), "geo news")

    def test_url_to_host(self):
        self.assertEqual(url_to_host("https://example.com/path/stream.m3u8"), "https://example.com")
        self.assertEqual(url_to_host("http://cdn.tv/live/123"), "http://cdn.tv")

    def test_detect_country_from_group(self):
        self.assertEqual(detect_country_from_group("bd"), "Bangladesh")
        self.assertEqual(detect_country_from_group("India"), "India")
        self.assertEqual(detect_country_from_group("American"), "United States")
        self.assertEqual(detect_country_from_group("br"), "Brazil")
        self.assertEqual(detect_country_from_group("movies"), "Movies")
        self.assertEqual(detect_country_from_group("sports"), "Sports")

    def test_has_special_headers(self):
        self.assertTrue(has_special_headers({"url": "http://example.com?token=abc"}))
        self.assertTrue(has_special_headers({
            "url": "http://example.com",
            "vlc_opts": ["#EXTVLCOPT:http-header=Cookie: session=123"]
        }))
        self.assertFalse(has_special_headers({"url": "http://example.com/stream.m3u8"}))

    def test_sanitize_text(self):
        self.assertEqual(sanitize_text(""), "Unknown")
        self.assertEqual(sanitize_text("  Hello World  "), "Hello World")
        self.assertIsNotNone(sanitize_text(None))


class TestParser(unittest.TestCase):
    """Test M3U parser."""

    def setUp(self):
        self.parser = M3UParser()

    def test_parse_basic_m3u(self):
        content = """#EXTM3U
#EXTINF:-1 tvg-id="bbc" group-title="News",BBC News
http://example.com/bbc.m3u8
#EXTINF:-1 group-title="Sports",Sky Sports
http://example.com/sky.m3u8
"""
        channels = self.parser.parse(content)
        self.assertEqual(len(channels), 2)
        self.assertEqual(channels[0]["name"], "BBC News")
        self.assertEqual(channels[0]["group"], "News")
        self.assertEqual(channels[1]["name"], "Sky Sports")

    def test_parse_with_cookies(self):
        content = """#EXTM3U
#EXTINF:-1 group-title="Premium",Premium Channel
#EXTVLCOPT:http-header=Cookie: token=abc123
http://example.com/premium.m3u8
"""
        channels = self.parser.parse(content)
        self.assertEqual(len(channels), 1)
        self.assertTrue(channels[0]["has_cookies"])

    def test_parse_with_logo(self):
        content = """#EXTM3U
#EXTINF:-1 tvg-logo="http://logo.png" group-title="BD",Channel Name
http://example.com/ch.m3u8
"""
        channels = self.parser.parse(content)
        self.assertEqual(channels[0]["tvg_logo"], "http://logo.png")
        self.assertEqual(channels[0]["group"], "Bangladesh")

    def test_parse_empty(self):
        channels = self.parser.parse("")
        self.assertEqual(len(channels), 0)

    def test_parse_all(self):
        sources = [
            {"source": "url1", "content": "#EXTM3U\n#EXTINF:-1 g='A',Ch1\nhttp://a.m3u8"},
            {"source": "url2", "content": "#EXTM3U\n#EXTINF:-1 g='B',Ch2\nhttp://b.m3u8"},
        ]
        channels = self.parser.parse_all(sources)
        self.assertEqual(len(channels), 2)


class TestEncryption(unittest.TestCase):
    """Test AES encryption/decryption module."""

    def test_generate_key(self):
        key = generate_key()
        self.assertEqual(len(key), 64)

    def test_encrypt_decrypt_cycle(self):
        key = generate_key()
        content = b"#EXTM3U\n#EXTINF:-1,Test Channel\nhttp://example.com/test.m3u8\n"
        
        with tempfile.NamedTemporaryFile(suffix='.m3u', delete=False) as f_in, \
             tempfile.NamedTemporaryFile(suffix='.enc', delete=False) as f_enc, \
             tempfile.NamedTemporaryFile(suffix='.m3u', delete=False) as f_out:
            
            f_in.write(content)
            f_in.close()
            f_enc.close()
            f_out.close()
            
            try:
                enc_res = encrypt_playlist(f_in.name, f_enc.name, key)
                self.assertIsNotNone(enc_res)
                
                dec_res = decrypt_playlist(f_enc.name, f_out.name, key)
                self.assertIsNotNone(dec_res)
                
                with open(f_out.name, 'rb') as f:
                    decrypted_content = f.read()
                    self.assertEqual(decrypted_content, content)
            finally:
                os.remove(f_in.name)
                os.remove(f_enc.name)
                os.remove(f_out.name)


class TestEPGFetcher(unittest.TestCase):
    """Test XMLTV EPG parser."""

    def test_parse_epg_xml(self):
        fetcher = EPGFetcher()
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<tv>
  <programme start="20260724220000 +0000" stop="20260724230000 +0000" channel="bbc.uk">
    <title>Late Night News</title>
    <desc>Global news coverage</desc>
  </programme>
</tv>"""
        programs = fetcher.parse_epg_programs(xml_content)
        self.assertEqual(len(programs), 1)
        self.assertEqual(programs[0]['title'], 'Late Night News')
        self.assertEqual(programs[0]['channel_id'], 'bbc.uk')


class TestXtreamParser(unittest.TestCase):
    """Test Xtream Codes API parser."""

    def test_convert_to_m3u_items(self):
        parser = XtreamParser("http://xtream.server:8080", "user1", "pass1")
        streams = [{
            'stream_id': 101,
            'name': 'HBO HD',
            'category_id': '5',
            'stream_icon': 'http://logo.png',
            'container_extension': 'm3u8'
        }]
        categories = [{'category_id': 5, 'category_name': 'Movies'}]

        items = parser.convert_to_m3u_items(streams, categories)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['name'], 'HBO HD')
        self.assertEqual(items[0]['group'], 'Movies')
        self.assertEqual(items[0]['url'], 'http://xtream.server:8080/live/user1/pass1/101.m3u8')


class TestTorrentBridge(unittest.TestCase):
    """Test Torrent & Acestream P2P link bridge."""

    def test_torrent_bridge(self):
        bridge = TorrentStreamBridge(local_proxy_port=8080)
        self.assertTrue(bridge.is_p2p_url("acestream://1234567890abcdef"))
        self.assertTrue(bridge.is_p2p_url("magnet:?xt=urn:btih:abcdef1234567890"))
        
        infohash = bridge.extract_infohash("acestream://1234567890abcdef")
        self.assertEqual(infohash, "1234567890abcdef")

        proxy_url = bridge.transform_to_http_proxy("acestream://1234567890abcdef")
        self.assertEqual(proxy_url, "http://127.0.0.1:8080/p2p/1234567890abcdef")


class TestSearchEngine(unittest.TestCase):
    """Test fuzzy channel search engine."""

    def test_fuzzy_search(self):
        channels = [
            {'name': 'HBO HD USA', 'group': 'United States'},
            {'name': 'BBC One UK', 'group': 'United Kingdom'},
            {'name': 'ESPN 1080p', 'group': 'Sports'}
        ]
        engine = ChannelSearchEngine(channels)
        results = engine.search("hbo")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'HBO HD USA')

        results_group = engine.filter_by_country("United Kingdom")
        self.assertEqual(len(results_group), 1)
        self.assertEqual(results_group[0]['name'], 'BBC One UK')


class TestContentFilter(unittest.TestCase):
    """Test parental control content filter."""

    def test_explicit_detection(self):
        filter_engine = ContentFilter(system_pin="0171")
        self.assertTrue(filter_engine.is_explicit({'name': 'Adult 18+ VIP', 'group': 'XXX'}))
        self.assertFalse(filter_engine.is_explicit({'name': 'Discovery Channel', 'group': 'Documentary'}))

        self.assertTrue(filter_engine.verify_pin("0171"))
        self.assertFalse(filter_engine.verify_pin("1234"))

        channels = [
            {'name': 'Safe TV', 'group': 'News'},
            {'name': 'Adult Movie 18+', 'group': 'XXX'}
        ]
        filtered = filter_engine.filter_channels(channels, pin_unlocked=False)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['name'], 'Safe TV')


class TestQualityClassifier(unittest.TestCase):
    """Test resolution and framerate quality classifier."""

    def test_quality_classification(self):
        classifier = StreamQualityClassifier()
        ch_4k = classifier.classify_channel({'name': 'Sky Sports 4K 60FPS', 'extinf': ''})
        self.assertEqual(ch_4k['quality'], '4K')
        self.assertTrue(ch_4k['is_60fps'])

        ch_fhd = classifier.classify_channel({'name': 'HBO FHD 1080p', 'extinf': ''})
        self.assertEqual(ch_fhd['quality'], 'FHD')


class TestIPFSPublisher(unittest.TestCase):
    """Test IPFS gateway resolution and URL formatting."""

    def test_ipfs_formatting(self):
        publisher = IPFSPublisher()
        cid = "QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco"
        formatted = publisher.format_ipfs_url(cid)
        self.assertTrue(formatted.startswith("https://"))
        self.assertIn(cid, formatted)

        gateways = publisher.get_all_gateway_urls(cid)
        self.assertGreaterEqual(len(gateways), 3)


class TestAIStreamHealer(unittest.TestCase):
    """Test Year 3050 Quantum Stream Health Index Scoring."""

    def test_quantum_score(self):
        healer = AIStreamHealer()
        s1 = Stream(url="https://hd.stream.tv/live.m3u8", name="High Quality Channel", latency_ms=50.0, tvg_logo="http://logo.png")
        s2 = Stream(url="http://slow.stream.tv/stream", name="Slow Channel", latency_ms=800.0)

        score1 = healer.compute_quantum_score(s1)
        score2 = healer.compute_quantum_score(s2)

        self.assertGreater(score1, score2)
        self.assertGreaterEqual(score1, 70.0)

        ranked = healer.rank_streams_by_quantum_score([s2, s1])
        self.assertEqual(ranked[0].url, s1.url)


if __name__ == "__main__":
    unittest.main()