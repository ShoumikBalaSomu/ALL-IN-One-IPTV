import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';
import '../../core/models/models.dart';

final playbackServiceProvider = Provider<PlaybackService>((ref) {
  return PlaybackService();
});

class PlaybackService {
  late final Player player;
  late final VideoController controller;
  
  Channel? currentChannel;

  PlaybackService() {
    // MediaKit requires initialization in main() before this point
    player = Player();
    controller = VideoController(player);

    // Listen to player errors to trigger smart fallback
    player.stream.error.listen((error) {
      print('Playback Error detected: $error');
      _triggerFallback();
    });

    // We can also listen to buffering states. If buffering stalls forever,
    // we could preemptively switch URLs.
    player.stream.buffering.listen((isBuffering) {
      // Implement advanced anti-stall logic here if needed
    });
  }

  void playChannel(Channel channel) {
    currentChannel = channel;
    // Reset index to primary URL
    channel.currentUrlIndex = 0; 
    _playCurrentUrl();
  }

  void _playCurrentUrl() {
    if (currentChannel == null) return;
    
    final url = currentChannel!.activeUrl;
    print('Attempting to play: $url');
    player.open(Media(url));
  }

  void _triggerFallback() {
    if (currentChannel == null) return;

    if (currentChannel!.currentUrlIndex < currentChannel!.fallbackUrls.length - 1) {
      print('Falling back to next available stream...');
      currentChannel!.currentUrlIndex++;
      _playCurrentUrl();
    } else {
      print('All fallback streams failed for channel: ${currentChannel!.name}');
      // Here we could notify the UI to show an error overlay or skip to the next channel entirely
    }
  }

  void dispose() {
    player.dispose();
  }
}
