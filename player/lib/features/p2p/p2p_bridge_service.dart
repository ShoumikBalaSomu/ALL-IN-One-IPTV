import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'torrent_streamer_server.dart';

final p2pBridgeProvider = Provider<P2PBridgeService>((ref) {
  final torrentServer = ref.watch(torrentStreamerProvider);
  return P2PBridgeService(torrentServer);
});

class P2PBridgeService {
  final TorrentStreamerServer _torrentServer;

  P2PBridgeService(this._torrentServer);

  /// Analyzes a stream URL and returns a playable HTTP URL for media_kit.
  /// If it's a P2P link (acestream:// or .torrent), it bridges it locally.
  Future<String> bridgeStreamUrl(String originalUrl) async {
    if (originalUrl.startsWith('acestream://')) {
      final infoHash = originalUrl.replaceFirst('acestream://', '');
      return await _torrentServer.startP2PStream(infoHash, isAcestream: true);
    } 
    
    if (originalUrl.endsWith('.torrent') || originalUrl.startsWith('magnet:?')) {
      return await _torrentServer.startP2PStream(originalUrl, isAcestream: false);
    }

    // Not a P2P stream, return the original standard HTTP/HTTPS URL
    return originalUrl;
  }

  void stopCurrentP2PStream() {
    _torrentServer.stopStreaming();
  }
}
