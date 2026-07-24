import 'dart:async';
import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';
import '../../../core/models/models.dart';

class VideoPlayerWidget extends StatefulWidget {
  final Channel? channel;
  final String? url;
  
  const VideoPlayerWidget({
    super.key, 
    this.channel, 
    this.url,
  }) : assert(channel != null || url != null, 'Either channel or url must be provided');

  @override
  State<VideoPlayerWidget> createState() => _VideoPlayerWidgetState();
}

class _VideoPlayerWidgetState extends State<VideoPlayerWidget> {
  late final Player player;
  late final VideoController controller;
  StreamSubscription? _errorSubscription;
  Timer? _fallbackTimer;

  int _currentFallbackIndex = 0;
  List<String> _urls = [];

  @override
  void initState() {
    super.initState();
    player = Player();
    controller = VideoController(player);
    _initPlayer();
  }

  void _initPlayer() {
    if (widget.channel != null) {
      _urls = widget.channel!.fallbackUrls.isNotEmpty 
          ? widget.channel!.fallbackUrls 
          : [];
    } else if (widget.url != null) {
      _urls = [widget.url!];
    }

    _currentFallbackIndex = 0;
    _playCurrentUrl();

    // Smart Fallback Engine: Subscribe to player errors
    _errorSubscription = player.stream.error.listen((error) {
      debugPrint("MediaKit Player Error encountered: $error");
      _handleStreamFailure();
    });
  }

  void _playCurrentUrl() {
    if (_urls.isNotEmpty && _currentFallbackIndex < _urls.length) {
      player.open(Media(_urls[_currentFallbackIndex]));
    }
  }

  void _handleStreamFailure() {
    _fallbackTimer?.cancel();
    _fallbackTimer = Timer(const Duration(milliseconds: 1500), () {
      if (!mounted) return;
      if (_currentFallbackIndex + 1 < _urls.length) {
        setState(() {
          _currentFallbackIndex++;
        });
        debugPrint("Auto Switching to Fallback Stream #${_currentFallbackIndex + 1}: ${_urls[_currentFallbackIndex]}");
        _playCurrentUrl();
      }
    });
  }

  @override
  void didUpdateWidget(covariant VideoPlayerWidget oldWidget) {
    super.didUpdateWidget(oldWidget);
    final oldUrl = oldWidget.channel?.activeUrl ?? oldWidget.url;
    final newUrl = widget.channel?.activeUrl ?? widget.url;

    if (newUrl != oldUrl) {
      _initPlayer();
    }
  }

  @override
  void dispose() {
    _errorSubscription?.cancel();
    _fallbackTimer?.cancel();
    player.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Video(
      controller: controller,
      controls: AdaptiveVideoControls,
      fit: BoxFit.contain,
    );
  }
}
