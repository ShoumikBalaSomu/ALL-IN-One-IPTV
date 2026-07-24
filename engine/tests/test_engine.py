import unittest
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from engine.src.parser import M3UParser, Stream
from engine.src.ai_healer import AIHealer
from engine.src.quality_classifier import QualityClassifier
from engine.src.deduplicator import Deduplicator
from engine.src.content_filter import ContentFilter
from engine.src.encryption import EncryptionVault
from engine.src.torrent_bridge import TorrentBridge

class TestEngine(unittest.TestCase):
    def test_parser(self):
        m3u = "#EXTM3U\n#EXTINF:-1 tvg-id=\"1\" group-title=\"News\",CNN\nhttp://test.com/cnn.m3u8"
        streams = M3UParser.parse(m3u)
        self.assertEqual(len(streams), 1)
        self.assertEqual(streams[0].name, "CNN")
        self.assertEqual(streams[0].tvg_id, "1")
        self.assertEqual(streams[0].group_title, "News")

    def test_ai_healer(self):
        healer = AIHealer()
        score = healer.calculate_qrs(True, 100, 0.5)
        self.assertGreater(score, 0)
        
        stream = Stream(url="dead", fallbacks=["alive"])
        healed = healer.heal_stream(stream, 5000, False)
        self.assertEqual(healed.url, "alive")
        self.assertEqual(healed.fallbacks[0], "dead")

    def test_quality_classifier(self):
        s = Stream(url="test", name="Movie 4K")
        QualityClassifier.classify(s)
        self.assertEqual(s.quality, "4K")

    def test_deduplicator(self):
        s1 = Stream(url="1", name="A", tvg_id="1")
        s2 = Stream(url="2", name="A", tvg_id="1")
        res = Deduplicator.deduplicate([s1, s2])
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].fallbacks, ["2"])

    def test_content_filter(self):
        s = Stream(url="1", name="Adult Channel XXX")
        cf = ContentFilter()
        res = cf.filter([s])
        self.assertIn("[LOCKED]", res[0].name)
        self.assertEqual(res[0].vlc_opts['pin'], "0171")

    def test_encryption(self):
        data = "my_secret_url"
        enc = EncryptionVault.xor_crypt(data)
        dec = EncryptionVault.xor_decrypt(enc)
        self.assertEqual(data, dec)

    def test_torrent_bridge(self):
        ace = TorrentBridge.acestream_to_http("test_id")
        self.assertIn("test_id", ace)

if __name__ == "__main__":
    unittest.main()