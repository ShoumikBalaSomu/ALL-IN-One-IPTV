import unittest
import asyncio
from src.parser import parse_m3u, Stream
from src.deduplicator import deduplicate

class TestEngine(unittest.TestCase):
    def test_parse_m3u(self):
        content = """#EXTM3U
#EXTINF:-1 tvg-id="Test.us" group-title="News",Test Channel
http://test.com/stream.m3u8"""
        streams = parse_m3u(content)
        self.assertEqual(len(streams), 1)
        self.assertEqual(streams[0].name, "Test Channel")
        self.assertEqual(streams[0].tvg_id, "Test.us")
        self.assertEqual(streams[0].group_title, "News")
        self.assertEqual(streams[0].url, "http://test.com/stream.m3u8")

    def test_deduplicate(self):
        streams = [
            Stream(url="http://test.com/1", name="Test 1"),
            Stream(url="http://test.com/1", name="Test 1 Duplicate"),
            Stream(url="http://test.com/2", name="Test 2")
        ]
        unique = deduplicate(streams)
        self.assertEqual(len(unique), 2)
        self.assertEqual(unique[0].url, "http://test.com/1")
        self.assertEqual(unique[1].url, "http://test.com/2")

if __name__ == '__main__':
    unittest.main()
