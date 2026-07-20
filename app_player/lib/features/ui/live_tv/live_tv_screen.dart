import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'channel_provider.dart';
import 'video_player_widget.dart';

class LiveTVScreen extends ConsumerWidget {
  const LiveTVScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final categories = ref.watch(categoriesProvider);
    final filteredChannels = ref.watch(filteredChannelsProvider);
    final selectedCategory = ref.watch(selectedCategoryProvider);
    final selectedChannel = ref.watch(selectedChannelProvider);
    final playlistAsync = ref.watch(playlistProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('ALL-IN-One IPTV'),
      ),
      body: playlistAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error loading playlist: $err')),
        data: (_) => Row(
          children: [
            // Sidebar for Categories/Countries
            Expanded(
              flex: 2,
              child: Container(
                color: Colors.grey[900],
                child: ListView(
                  children: [
                    ListTile(
                      title: const Text('All Channels'),
                      selected: selectedCategory == null,
                      onTap: () => ref.read(selectedCategoryProvider.notifier).state = null,
                    ),
                    ...categories.map((category) => ListTile(
                          title: Text(category),
                          selected: selectedCategory == category,
                          onTap: () => ref.read(selectedCategoryProvider.notifier).state = category,
                        )),
                  ],
                ),
              ),
            ),
            // Center for Channels
            Expanded(
              flex: 3,
              child: Container(
                color: Colors.grey[850],
                child: ListView.builder(
                  itemCount: filteredChannels.length,
                  itemBuilder: (context, index) {
                    final channel = filteredChannels[index];
                    return ListTile(
                      leading: channel.logoUrl.isNotEmpty
                          ? Image.network(
                              channel.logoUrl,
                              width: 40,
                              height: 40,
                              errorBuilder: (_, __, ___) => const Icon(Icons.tv),
                            )
                          : const Icon(Icons.tv),
                      title: Text(channel.name),
                      subtitle: Text(channel.group),
                      selected: selectedChannel?.tvgId == channel.tvgId && selectedChannel?.name == channel.name,
                      onTap: () => ref.read(selectedChannelProvider.notifier).state = channel,
                    );
                  },
                ),
              ),
            ),
            // Right panel for Mini Player and Info
            Expanded(
              flex: 4,
              child: Container(
                color: Colors.black,
                child: Column(
                  children: [
                    // Mini Player
                    Container(
                      height: 300,
                      color: Colors.black87,
                      child: selectedChannel != null
                          ? VideoPlayerWidget(url: selectedChannel.activeUrl)
                          : const Center(
                              child: Text('Select a channel to play'),
                            ),
                    ),
                    // EPG Info
                    Expanded(
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: selectedChannel != null
                            ? Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    selectedChannel.name,
                                    style: Theme.of(context).textTheme.headlineSmall,
                                  ),
                                  const SizedBox(height: 8),
                                  Text('Category: ${selectedChannel.group}'),
                                  const SizedBox(height: 8),
                                  Text('Sources: ${selectedChannel.fallbackUrls.length}'),
                                  const SizedBox(height: 16),
                                  const Text('EPG Data: Not available yet.'),
                                ],
                              )
                            : const Text('No channel selected.'),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
