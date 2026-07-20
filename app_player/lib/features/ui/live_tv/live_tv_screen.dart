import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'dart:ui';
import 'channel_provider.dart';
import 'video_player_widget.dart';

class LiveTVScreen extends ConsumerStatefulWidget {
  const LiveTVScreen({super.key});

  @override
  ConsumerState<LiveTVScreen> createState() => _LiveTVScreenState();
}

class _LiveTVScreenState extends ConsumerState<LiveTVScreen> {
  bool _showEPG = true;

  @override
  Widget build(BuildContext context) {
    final categories = ref.watch(categoriesProvider);
    final filteredChannels = ref.watch(filteredChannelsProvider);
    final selectedCategory = ref.watch(selectedCategoryProvider);
    final selectedChannel = ref.watch(selectedChannelProvider);
    final playlistAsync = ref.watch(playlistProvider);

    return Scaffold(
      backgroundColor: const Color(0xFF0A0A0F),
      body: playlistAsync.when(
        loading: () => const Center(child: CircularProgressIndicator(color: Colors.redAccent)),
        error: (err, stack) => Center(child: Text('Error loading playlist: $err', style: const TextStyle(color: Colors.white))),
        data: (_) => Row(
          children: [
            // Sidebar for Categories/Countries with Glassmorphism
            Container(
              width: 260,
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.05),
                border: Border(right: BorderSide(color: Colors.white.withOpacity(0.1), width: 1)),
              ),
              child: ClipRRect(
                child: BackdropFilter(
                  filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
                  child: Column(
                    children: [
                      Padding(
                        padding: const EdgeInsets.all(20.0),
                        child: Row(
                          children: [
                            const Icon(Icons.live_tv, color: Colors.redAccent, size: 28),
                            const SizedBox(width: 10),
                            const Text('Live TV', style: TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
                          ],
                        ),
                      ),
                      const Divider(color: Colors.white24, height: 1),
                      Expanded(
                        child: ListView(
                          padding: const EdgeInsets.symmetric(vertical: 10),
                          children: [
                            _buildCategoryTile('All Channels', selectedCategory == null, () => ref.read(selectedCategoryProvider.notifier).state = null),
                            ...categories.map((category) => _buildCategoryTile(category, selectedCategory == category, () => ref.read(selectedCategoryProvider.notifier).state = category)),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
            
            // Center List of Channels
            Container(
              width: 320,
              color: const Color(0xFF12131A),
              child: Column(
                children: [
                  Padding(
                    padding: const EdgeInsets.all(12.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('Channels', style: TextStyle(color: Colors.white70, fontSize: 16, fontWeight: FontWeight.w600)),
                        Row(
                          children: [
                            IconButton(icon: const Icon(Icons.sort, color: Colors.white70, size: 20), onPressed: () {}, tooltip: 'Sort'),
                            IconButton(icon: const Icon(Icons.filter_alt_outlined, color: Colors.white70, size: 20), onPressed: () {}, tooltip: 'Filter'),
                          ],
                        )
                      ],
                    ),
                  ),
                  Expanded(
                    child: ListView.builder(
                      itemCount: filteredChannels.length,
                      itemBuilder: (context, index) {
                        final channel = filteredChannels[index];
                        final isSelected = selectedChannel?.tvgId == channel.tvgId && selectedChannel?.name == channel.name;
                        
                        return Container(
                          margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                          decoration: BoxDecoration(
                            color: isSelected ? Colors.redAccent.withOpacity(0.2) : Colors.transparent,
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: isSelected ? Colors.redAccent : Colors.transparent),
                          ),
                          child: ListTile(
                            leading: Container(
                              width: 45,
                              height: 45,
                              decoration: BoxDecoration(
                                color: Colors.black45,
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: channel.logoUrl.isNotEmpty
                                  ? ClipRRect(
                                      borderRadius: BorderRadius.circular(8),
                                      child: Image.network(channel.logoUrl, fit: BoxFit.cover, errorBuilder: (_, __, ___) => const Icon(Icons.tv, color: Colors.white54)))
                                  : const Icon(Icons.tv, color: Colors.white54),
                            ),
                            title: Text('${index + 1}. ${channel.name}', style: TextStyle(color: isSelected ? Colors.white : Colors.white70, fontWeight: isSelected ? FontWeight.bold : FontWeight.normal), maxLines: 1, overflow: TextOverflow.ellipsis),
                            subtitle: Text(channel.group, style: TextStyle(color: Colors.white38, fontSize: 12), maxLines: 1),
                            onTap: () => ref.read(selectedChannelProvider.notifier).state = channel,
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),
            
            // Right Panel (Video Player + EPG + Details)
            Expanded(
              child: Container(
                color: const Color(0xFF0A0A0F),
                child: Column(
                  children: [
                    // Video Player
                    Container(
                      height: MediaQuery.of(context).size.height * 0.5,
                      color: Colors.black,
                      child: selectedChannel != null
                          ? VideoPlayerWidget(url: selectedChannel.activeUrl)
                          : const Center(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(Icons.live_tv, size: 64, color: Colors.white24),
                                  SizedBox(height: 16),
                                  Text('Select a channel to start playing', style: TextStyle(color: Colors.white54, fontSize: 18)),
                                ],
                              ),
                            ),
                    ),
                    
                    // Toolbar
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                      color: const Color(0xFF15161E),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Row(
                            children: [
                              IconButton(
                                icon: Icon(_showEPG ? Icons.list_alt : Icons.list_alt_outlined, color: _showEPG ? Colors.redAccent : Colors.white70),
                                onPressed: () => setState(() => _showEPG = !_showEPG),
                                tooltip: 'Toggle EPG',
                              ),
                              IconButton(icon: const Icon(Icons.aspect_ratio, color: Colors.white70), onPressed: () {}, tooltip: 'Aspect Ratio'),
                            ],
                          ),
                          Row(
                            children: [
                              IconButton(icon: const Icon(Icons.block, color: Colors.white70), onPressed: () {}, tooltip: 'Block Channel'),
                              IconButton(icon: const Icon(Icons.settings, color: Colors.white70), onPressed: () {}, tooltip: 'Settings'),
                            ],
                          )
                        ],
                      ),
                    ),
                    
                    // EPG and Details
                    if (_showEPG && selectedChannel != null)
                      Expanded(
                        child: Container(
                          padding: const EdgeInsets.all(20),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(selectedChannel.name, style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
                              const SizedBox(height: 8),
                              Row(
                                children: [
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                    decoration: BoxDecoration(color: Colors.white12, borderRadius: BorderRadius.circular(4)),
                                    child: Text(selectedChannel.group, style: const TextStyle(color: Colors.white70, fontSize: 12)),
                                  ),
                                  const SizedBox(width: 10),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                    decoration: BoxDecoration(color: Colors.green.withOpacity(0.2), borderRadius: BorderRadius.circular(4)),
                                    child: Text('${selectedChannel.fallbackUrls.length} Sources Folded', style: const TextStyle(color: Colors.greenAccent, fontSize: 12)),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 30),
                              const Text('Now Playing', style: TextStyle(color: Colors.white54, fontSize: 14, fontWeight: FontWeight.w600, textBaseline: TextBaseline.alphabetic)),
                              const SizedBox(height: 10),
                              Container(
                                padding: const EdgeInsets.all(16),
                                decoration: BoxDecoration(
                                  color: Colors.white.withOpacity(0.05),
                                  borderRadius: BorderRadius.circular(8),
                                  border: Border.all(color: Colors.white10),
                                ),
                                child: const Row(
                                  children: [
                                    Text('10:00 - 12:00', style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold)),
                                    SizedBox(width: 20),
                                    Text('Morning News / Show', style: TextStyle(color: Colors.white, fontSize: 16)),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                      )
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCategoryTile(String title, bool isSelected, VoidCallback onTap) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      decoration: BoxDecoration(
        color: isSelected ? Colors.redAccent : Colors.transparent,
        borderRadius: BorderRadius.circular(8),
      ),
      child: ListTile(
        title: Text(title, style: TextStyle(color: isSelected ? Colors.white : Colors.white70, fontWeight: isSelected ? FontWeight.bold : FontWeight.normal)),
        onTap: onTap,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      ),
    );
  }
}
