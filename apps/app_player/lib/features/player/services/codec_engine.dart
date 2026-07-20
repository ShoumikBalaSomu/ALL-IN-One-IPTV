import 'dart:convert';
import 'package:media_kit/media_kit.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

class CodecEngine {
  final Player player;
  WebSocketChannel? _wsChannel;
  String _currentChannelName = "";

  CodecEngine(this.player) {
    _initializeHardwareDecoding();
    _connectToStreamHealer();
  }

  /// Forcefully enable OS native hardware APIs for AV1/HEVC/VVC
  void _initializeHardwareDecoding() {
    // MediaCodec (Android), DXVA2 (Windows), VAAPI (Linux)
    player.setProperty('hwdec', 'auto');
    player.setProperty('hwdec-codecs', 'all'); 
    print("CodecEngine: AV1 Hardware Acceleration Enabled");
  }

  /// Sets up a persistent WebSocket connection to the AI Stream Healer backend
  void _connectToStreamHealer() {
    try {
      final wsUrl = Uri.parse('ws://YOUR_SERVER_IP:8765');
      _wsChannel = WebSocketChannel.connect(wsUrl);
      
      _wsChannel!.stream.listen((message) {
        final data = jsonDecode(message);
        if (data['type'] == 'hot_swap' && data['channel_name'] == _currentChannelName) {
          _hotSwapStream(data['new_url']);
        }
      });
    } catch (e) {
      print("CodecEngine: Failed to connect to Stream Healer - $e");
    }
  }

  /// Called by the UI when a user selects a channel
  void playStream(String url, String channelName) {
    _currentChannelName = channelName;
    player.open(Media(url));
  }

  /// Silently swaps the underlying media source without destroying the UI widget
  void _hotSwapStream(String newUrl) {
    print("CodecEngine: Hot-Swapping dead stream -> $newUrl");
    // Preserve current playback position if it's VOD, or just snap to live
    player.open(Media(newUrl), play: true);
  }

  /// Called by the player listener if it detects a freeze or 404
  void reportCrash() {
    if (_wsChannel != null && _currentChannelName.isNotEmpty) {
      print("CodecEngine: Reporting crash for $_currentChannelName...");
      _wsChannel!.sink.add(jsonEncode({
        "type": "crash_report",
        "channel_name": _currentChannelName
      }));
    }
  }

  void dispose() {
    _wsChannel?.sink.close();
  }
}
