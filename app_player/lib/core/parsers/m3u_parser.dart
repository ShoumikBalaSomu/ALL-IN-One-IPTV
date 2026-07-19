import 'package:dio/dio.dart';
import '../models/models.dart';

class M3UParser {
  final Dio dio;

  M3UParser({required this.dio});

  /// Fetches an M3U file from a URL or local proxy, parses it, and folds duplicates.
  Future<List<Channel>> parsePlaylist(String url) async {
    try {
      final response = await dio.get(url);
      final content = response.data as String;
      return _parseAndFold(content);
    } catch (e) {
      throw Exception('Failed to load playlist: $e');
    }
  }

  List<Channel> _parseAndFold(String content) {
    final lines = content.split('\n');
    final Map<String, Channel> foldedChannels = {};

    String? currentExtinf;

    for (var line in lines) {
      line = line.trim();
      if (line.isEmpty) continue;

      if (line.startsWith('#EXTINF')) {
        currentExtinf = line;
      } else if (!line.startsWith('#') && currentExtinf != null) {
        // Extract basic metadata using regex
        final nameMatch = RegExp(r',(.*)$').firstMatch(currentExtinf);
        final name = nameMatch?.group(1)?.trim() ?? 'Unknown';

        final groupMatch = RegExp(r'group-title="([^"]+)"').firstMatch(currentExtinf);
        final countryMatch = RegExp(r'tvg-country="([^"]+)"').firstMatch(currentExtinf);
        final group = countryMatch?.group(1) ?? groupMatch?.group(1) ?? 'Uncategorized';

        final idMatch = RegExp(r'tvg-id="([^"]+)"').firstMatch(currentExtinf);
        final tvgId = idMatch?.group(1) ?? '';

        final logoMatch = RegExp(r'tvg-logo="([^"]+)"').firstMatch(currentExtinf);
        final logo = logoMatch?.group(1) ?? '';
        
        final uniqueKey = '$group-$name';

        // Fold Logic: If channel already exists, just append the URL to the fallback array
        if (foldedChannels.containsKey(uniqueKey)) {
          if (!foldedChannels[uniqueKey]!.fallbackUrls.contains(line)) {
            foldedChannels[uniqueKey]!.fallbackUrls.add(line);
          }
        } else {
          foldedChannels[uniqueKey] = Channel()
            ..name = name
            ..group = group
            ..tvgId = tvgId
            ..logoUrl = logo
            ..fallbackUrls = [line];
        }

        currentExtinf = null;
      }
    }

    return foldedChannels.values.toList();
  }
}
