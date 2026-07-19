import 'package:dio/dio.dart';
import '../models/models.dart';

class XtreamParser {
  final Dio dio;
  final String baseUrl;
  final String username;
  final String password;

  XtreamParser({
    required this.dio,
    required this.baseUrl,
    required this.username,
    required this.password,
  });

  /// Authenticate and retrieve basic server/user info
  Future<Map<String, dynamic>> authenticate() async {
    final response = await dio.get(
      '$baseUrl/player_api.php',
      queryParameters: {'username': username, 'password': password},
    );
    return response.data;
  }

  /// Fetch Live TV channels and map them to our internal Channel model
  Future<List<Channel>> fetchLiveChannels() async {
    final response = await dio.get(
      '$baseUrl/player_api.php',
      queryParameters: {
        'username': username,
        'password': password,
        'action': 'get_live_streams'
      },
    );

    final List<dynamic> data = response.data;
    
    return data.map((json) {
      final streamId = json['stream_id'];
      return Channel()
        ..name = json['name'] ?? 'Unknown'
        ..tvgId = json['epg_channel_id']?.toString() ?? ''
        ..logoUrl = json['stream_icon'] ?? ''
        ..group = json['category_id']?.toString() ?? 'Uncategorized'
        // Xtream stream format: baseUrl/live/username/password/streamId.ts
        ..fallbackUrls = [
          '$baseUrl/live/$username/$password/$streamId.ts'
        ];
    }).toList();
  }
}
