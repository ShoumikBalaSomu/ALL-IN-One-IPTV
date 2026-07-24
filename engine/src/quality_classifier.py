import re
from .parser import Stream

class QualityClassifier:
    RESOLUTION_MAP = {
        r'4k|2160p': '4K',
        r'1080p|fhd': '1080p',
        r'720p|hd': '720p',
        r'480p|sd': 'SD'
    }

    @classmethod
    def classify(cls, stream: Stream) -> Stream:
        lower_name = stream.name.lower()
        for pattern, res in cls.RESOLUTION_MAP.items():
            if re.search(pattern, lower_name):
                stream.quality = res
                return stream
        stream.quality = 'SD' # Default
        return stream
