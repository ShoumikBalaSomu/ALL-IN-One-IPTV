import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';

class MultiViewGrid extends StatefulWidget {
  final List<String> streamUrls;

  const MultiViewGrid({Key? key, required this.streamUrls}) : super(key: key);

  @override
  _MultiViewGridState createState() => _MultiViewGridState();
}

class _MultiViewGridState extends State<MultiViewGrid> {
  final List<Player> _players = [];
  final List<VideoController> _controllers = [];
  int _focusedIndex = 0;

  @override
  void initState() {
    super.initState();
    _initializePlayers();
  }

  void _initializePlayers() {
    // Hard-cap at 4 concurrent streams to prevent VRAM exhaustion
    final limit = widget.streamUrls.length > 4 ? 4 : widget.streamUrls.length;

    for (int i = 0; i < limit; i++) {
      final player = Player();
      final controller = VideoController(player);
      
      // Start buffering and decoding
      player.open(Media(widget.streamUrls[i]), play: true);
      
      // Initial Audio Focus: Only the first stream is unmuted
      player.setVolume(i == 0 ? 100 : 0);

      _players.add(player);
      _controllers.add(controller);
    }
  }

  void _updateAudioFocus(int newIndex) {
    if (_focusedIndex == newIndex) return;

    setState(() {
      // Mute old focus
      _players[_focusedIndex].setVolume(0);
      // Unmute new focus
      _players[newIndex].setVolume(100);
      _focusedIndex = newIndex;
    });
  }

  @override
  void dispose() {
    for (var player in _players) {
      player.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // 2x2 Grid Layout
    return GridView.builder(
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        childAspectRatio: 16 / 9,
      ),
      itemCount: _controllers.length,
      itemBuilder: (context, index) {
        return MouseRegion(
          onEnter: (_) => _updateAudioFocus(index),
          child: GestureDetector(
            onTap: () => _updateAudioFocus(index),
            child: Container(
              decoration: BoxDecoration(
                border: Border.all(
                  color: _focusedIndex == index ? Colors.blueAccent : Colors.transparent,
                  width: 3,
                ),
              ),
              child: Video(controller: _controllers[index]),
            ),
          ),
        );
      },
    );
  }
}
