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
from engine.src.parser import M3UParser
from engine.src.encryption import encrypt_playlist, decrypt_playlist, generate_key


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


if __name__ == "__main__":
    unittest.main()