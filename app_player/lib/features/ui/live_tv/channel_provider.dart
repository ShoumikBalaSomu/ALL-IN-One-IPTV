import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';
import '../../../core/models/models.dart';
import '../../../core/parsers/m3u_parser.dart';

// Provides the list of channels parsed from the raw github playlist.
final playlistProvider = FutureProvider<List<Channel>>((ref) async {
  final dio = Dio();
  final parser = M3UParser(dio: dio);
  const url = 'https://raw.githubusercontent.com/ShoumikBalaSomu/ALL-IN-One-IPTV/main/output/checked_combined_by_country.m3u';
  final channels = await parser.parsePlaylist(url);
  return channels;
});

// Provides the currently selected category/group (country)
final selectedCategoryProvider = StateProvider<String?>((ref) => null);

// Provides the currently selected channel for playback
final selectedChannelProvider = StateProvider<Channel?>((ref) => null);

// A computed provider that filters the channels based on the selected category
final filteredChannelsProvider = Provider<List<Channel>>((ref) {
  final channelsAsyncValue = ref.watch(playlistProvider);
  final selectedCategory = ref.watch(selectedCategoryProvider);

  return channelsAsyncValue.when(
    data: (channels) {
      if (selectedCategory == null) return channels;
      return channels.where((c) => c.group == selectedCategory).toList();
    },
    loading: () => [],
    error: (_, __) => [],
  );
});

// A computed provider that extracts all unique categories
final categoriesProvider = Provider<List<String>>((ref) {
  final channelsAsyncValue = ref.watch(playlistProvider);
  return channelsAsyncValue.when(
    data: (channels) {
      final groups = channels.map((c) => c.group).toSet().toList();
      groups.sort();
      return groups;
    },
    loading: () => [],
    error: (_, __) => [],
  );
});
