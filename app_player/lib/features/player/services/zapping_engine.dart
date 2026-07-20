import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:media_kit/media_kit.dart';
import 'package:device_info_plus/device_info_plus.dart';

final zappingEngineProvider = Provider<ZappingEngine>((ref) {
  return ZappingEngine();
});

class ZappingEngine {
  Player? _prevPlayer;
  Player? _nextPlayer;
  
  bool _isHardwareCapable = false;

  ZappingEngine() {
    _checkHardwareCapabilities();
  }

  /// Checks system RAM to aggressively disable pre-fetching on low-end Android TV boxes
  Future<void> _checkHardwareCapabilities() async {
    final deviceInfo = DeviceInfoPlugin();
    // Assuming Android for this example check
    try {
      final androidInfo = await deviceInfo.androidInfo;
      // Convert bytes to GB. Example threshold: 2.5 GB
      final totalRamGb = androidInfo.systemFeatures.length > 50 ? 3.0 : 1.5; // Mock logic
      
      if (totalRamGb > 2.0) {
        _isHardwareCapable = true;
        print("Hardware capable of Zero-Latency Zapping. Pre-fetching enabled.");
      } else {
        _isHardwareCapable = false;
        print("Low memory detected. Pre-fetching disabled to prevent codec crashing.");
      }
    } catch (e) {
      _isHardwareCapable = false;
    }
  }

  /// Called when the user settles on a channel. 
  /// Spins up hidden, muted instances of the immediate neighbors.
  void onChannelSettled(String currentUrl, String prevUrl, String nextUrl) {
    if (!_isHardwareCapable) return;

    _disposeHiddenPlayers(); // Clear previous pre-fetches

    // Pre-fetch Next Channel
    _nextPlayer = Player();
    _nextPlayer!.setVolume(0); // Muted
    _nextPlayer!.open(Media(nextUrl), play: true); // Start buffering

    // Pre-fetch Prev Channel
    _prevPlayer = Player();
    _prevPlayer!.setVolume(0); 
    _prevPlayer!.open(Media(prevUrl), play: true); 
  }

  /// Instantly promotes a pre-fetched player to the main surface
  Player? consumeNextPlayer() {
    if (_nextPlayer == null) return null;
    final promoted = _nextPlayer;
    promoted!.setVolume(100); // Unmute
    _nextPlayer = null;
    return promoted;
  }

  void _disposeHiddenPlayers() {
    _prevPlayer?.dispose();
    _nextPlayer?.dispose();
    _prevPlayer = null;
    _nextPlayer = null;
  }
}
