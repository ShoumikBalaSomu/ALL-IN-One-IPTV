"""
Quality Classifier Engine.
Analyzes stream metadata and channel titles to classify resolution (4K, 1080p/FHD, 720p/HD, SD, 60FPS).
"""

import re

class StreamQualityClassifier:
    """Classifies stream resolution and frame rate."""

    QUALITY_PATTERNS = {
        '4K': re.compile(r'\b(4k|uhd|2160p|ultrahd)\b', re.IGNORECASE),
        'FHD': re.compile(r'\b(fhd|1080p|full\s*hd)\b', re.IGNORECASE),
        'HD': re.compile(r'\b(hd|720p)\b', re.IGNORECASE),
        'SD': re.compile(r'\b(sd|480p|360p|hq)\b', re.IGNORECASE),
        '60FPS': re.compile(r'\b(60fps|60\s*fps|50fps)\b', re.IGNORECASE)
    }

    def classify_channel(self, channel: dict) -> dict:
        """Add resolution and framerate tags to channel metadata."""
        title = channel.get('name', '')
        extinf = channel.get('extinf', '')
        combined_text = f"{title} {extinf}"

        detected_quality = "SD" # Default
        for q_name, pattern in self.QUALITY_PATTERNS.items():
            if q_name == '60FPS':
                continue
            if pattern.search(combined_text):
                detected_quality = q_name
                break

        is_60fps = bool(self.QUALITY_PATTERNS['60FPS'].search(combined_text))

        # Copy channel dict and add quality metadata
        enhanced = dict(channel)
        enhanced['quality'] = detected_quality
        enhanced['is_60fps'] = is_60fps

        # Append quality badge to tvg-name if missing
        if f"[{detected_quality}]" not in title and detected_quality != "SD":
            enhanced['display_name'] = f"{title} [{detected_quality}]"
        else:
            enhanced['display_name'] = title

        return enhanced

    def batch_classify(self, channels: list[dict]) -> list[dict]:
        """Classify a collection of channels."""
        return [self.classify_channel(ch) for ch in channels]
