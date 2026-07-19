import 'package:media_kit/media_kit.dart';
import 'package:device_info_plus/device_info_plus.dart';

class MediaProcessor {
  final Player player;
  bool _isLowPowerDevice = false;

  MediaProcessor(this.player) {
    _detectDevicePower();
  }

  Future<void> _detectDevicePower() async {
    // Basic throttle switch for ARM/Low-end Android
    final deviceInfo = DeviceInfoPlugin();
    try {
      final androidInfo = await deviceInfo.androidInfo;
      // Mock logic: RAM < 2GB is considered low power
      final totalRamGb = androidInfo.systemFeatures.length > 50 ? 3.0 : 1.5;
      _isLowPowerDevice = totalRamGb <= 2.0;
    } catch (e) {
      _isLowPowerDevice = true; // Safe fallback
    }
  }

  /// Injects EBU R128 dynamic loudness normalization to prevent deafening volume spikes
  void applyAudioNormalization() {
    // EBU R128 Loudnorm FFmpeg Filter
    // I=-16 (Integrated Loudness)
    // TP=-1.5 (True Peak Limit)
    // LRA=11 (Loudness Range)
    const loudnormFilter = 'loudnorm=I=-16:TP=-1.5:LRA=11';
    
    // Pass standard MPV property
    player.setProperty('af', loudnormFilter);
    print("MediaProcessor: Applied EBU R128 Audio Normalization.");
  }

  /// Analyzes incoming stream resolution and dynamically applies Lanczos upscaling if < 1080p
  void applyVideoUpscaling(int width, int height) {
    if (_isLowPowerDevice) {
      print("MediaProcessor: Low-power device detected. Hardware upscaling disabled.");
      return;
    }

    if (height < 1080) {
      // Apply edge-preserving bicubic/Lanczos upscaling
      const scaleFilter = 'scale=1920:1080:flags=lanczos';
      player.setProperty('vf', scaleFilter);
      print("MediaProcessor: Applied 1080p Lanczos Upscaling to $width x $height stream.");
    }
  }

  /// Monitors frame drops to gracefully degrade scaling on the fly
  void monitorFrameDrops(int droppedFrames, int totalFrames) {
    if (totalFrames == 0) return;
    final dropRate = droppedFrames / totalFrames;
    
    if (dropRate > 0.05) {
      print("MediaProcessor: 5% frame drop limit reached. Degrading video pipeline.");
      player.setProperty('vf', ''); // Remove heavy video filters
    }
  }
}
