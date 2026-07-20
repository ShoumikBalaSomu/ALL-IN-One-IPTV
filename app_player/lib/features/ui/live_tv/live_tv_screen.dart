import 'package:flutter/material.dart';
import 'dart:ui';
import '../vod/vod_screen.dart';

class LiveTVScreen extends StatefulWidget {
  const LiveTVScreen({super.key});

  @override
  State<LiveTVScreen> createState() => _LiveTVScreenState();
}

class _LiveTVScreenState extends State<LiveTVScreen> {
  int _selectedCategoryIndex = 0;
  int _selectedChannelIndex = 0;
  bool _isSidebarExpanded = false;

  final List<String> _categories = ['All Channels', 'Sports', 'News', 'Movies', 'Documentaries', 'Kids', 'Music', 'International'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F1014),
      body: Stack(
        children: [
          // Background subtle animated gradient
          Positioned.fill(
            child: Container(
              decoration: const BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [Color(0xFF0F1014), Color(0xFF1A1B22)],
                ),
              ),
            ),
          ),
          
          Row(
            children: [
              _buildSidebar(),
              Expanded(
                child: Column(
                  children: [
                    _buildTopBar(),
                    Expanded(
                      child: Row(
                        children: [
                          _buildChannelList(),
                          _buildPreviewAndEPG(),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildTopBar() {
    return Container(
      height: 70,
      padding: const EdgeInsets.symmetric(horizontal: 24),
      child: Row(
        children: [
          Text(
            _categories[_selectedCategoryIndex].toUpperCase(),
            style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.w900, letterSpacing: 1.5),
          ),
          const Spacer(),
          IconButton(icon: const Icon(Icons.sort, color: Colors.white70), onPressed: () {}),
          IconButton(icon: const Icon(Icons.filter_alt_outlined, color: Colors.white70), onPressed: () {}),
          const SizedBox(width: 16),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.1),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Row(
              children: const [
                Icon(Icons.search, size: 18, color: Colors.white70),
                SizedBox(width: 8),
                Text('Search channels...', style: TextStyle(color: Colors.white54, fontSize: 14)),
              ],
            ),
          ),
          const SizedBox(width: 16),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFFE50914),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
            ),
            onPressed: () {
              Navigator.push(context, PageRouteBuilder(
                pageBuilder: (context, a, b) => const VODScreen(),
                transitionsBuilder: (context, anim, b, child) => FadeTransition(opacity: anim, child: child),
              ));
            },
            child: const Text('Switch to VOD', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
          )
        ],
      ),
    );
  }

  Widget _buildSidebar() {
    return MouseRegion(
      onEnter: (_) => setState(() => _isSidebarExpanded = true),
      onExit: (_) => setState(() => _isSidebarExpanded = false),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOutCubic,
        width: _isSidebarExpanded ? 220 : 70,
        decoration: BoxDecoration(
          color: Colors.black.withOpacity(0.4),
          border: Border(right: BorderSide(color: Colors.white.withOpacity(0.05))),
        ),
        child: ClipRRect(
          child: BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 20, sigmaY: 20),
            child: Column(
              children: [
                const SizedBox(height: 30),
                const Icon(Icons.tv, color: Color(0xFFE50914), size: 32),
                const SizedBox(height: 40),
                Expanded(
                  child: ListView.builder(
                    physics: const BouncingScrollPhysics(),
                    itemCount: _categories.length,
                    itemBuilder: (context, index) {
                      final isSelected = index == _selectedCategoryIndex;
                      return InkWell(
                        onTap: () => setState(() => _selectedCategoryIndex = index),
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 200),
                          margin: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
                          padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 12),
                          decoration: BoxDecoration(
                            color: isSelected ? const Color(0xFFE50914).withOpacity(0.2) : Colors.transparent,
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(color: isSelected ? const Color(0xFFE50914).withOpacity(0.5) : Colors.transparent),
                          ),
                          child: Row(
                            children: [
                              Icon(
                                _getIconForCategory(index),
                                color: isSelected ? const Color(0xFFE50914) : Colors.white54,
                                size: 24,
                              ),
                              if (_isSidebarExpanded) ...[
                                const SizedBox(width: 16),
                                Expanded(
                                  child: Text(
                                    _categories[index],
                                    style: TextStyle(
                                      color: isSelected ? Colors.white : Colors.white54,
                                      fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                                      fontSize: 14,
                                    ),
                                    maxLines: 1,
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                ),
                              ]
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  IconData _getIconForCategory(int index) {
    switch (index) {
      case 0: return Icons.apps;
      case 1: return Icons.sports_soccer;
      case 2: return Icons.article;
      case 3: return Icons.movie;
      case 4: return Icons.public;
      case 5: return Icons.child_care;
      case 6: return Icons.music_note;
      default: return Icons.language;
    }
  }

  Widget _buildChannelList() {
    return Expanded(
      flex: 4,
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        physics: const BouncingScrollPhysics(),
        itemCount: 50,
        itemBuilder: (context, index) {
          final isSelected = index == _selectedChannelIndex;
          return Padding(
            padding: const EdgeInsets.only(bottom: 8.0),
            child: InkWell(
              onTap: () => setState(() => _selectedChannelIndex = index),
              borderRadius: BorderRadius.circular(12),
              child: AnimatedContainer(
                duration: const Duration(milliseconds: 200),
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: isSelected ? Colors.white.withOpacity(0.1) : Colors.transparent,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: isSelected ? Colors.white.withOpacity(0.2) : Colors.transparent),
                ),
                child: Row(
                  children: [
                    Text('${index + 1}'.padLeft(3, '0'), style: const TextStyle(color: Colors.white30, fontFamily: 'monospace')),
                    const SizedBox(width: 16),
                    Container(
                      width: 50,
                      height: 50,
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(8),
                        image: DecorationImage(image: NetworkImage('https://picsum.photos/100?random=$index')),
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('Premium Channel ${index + 1}', style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
                          const SizedBox(height: 4),
                          Text(isSelected ? 'Now Playing: Evening News Live' : 'Up Next: Blockbuster Movie', style: TextStyle(color: isSelected ? const Color(0xFF00FF7F) : Colors.white54, fontSize: 13)),
                        ],
                      ),
                    ),
                    if (isSelected) const Icon(Icons.volume_up, color: Colors.white, size: 20),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildPreviewAndEPG() {
    return Expanded(
      flex: 3,
      child: Container(
        margin: const EdgeInsets.fromLTRB(0, 16, 24, 24),
        decoration: BoxDecoration(
          color: const Color(0xFF1E1E24),
          borderRadius: BorderRadius.circular(24),
          border: Border.all(color: Colors.white.withOpacity(0.05)),
          boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.5), blurRadius: 30, offset: const Offset(0, 10))],
        ),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(24),
          child: Column(
            children: [
              // Fake Video Player
              Container(
                height: 250,
                width: double.infinity,
                color: Colors.black,
                child: Stack(
                  alignment: Alignment.center,
                  children: [
                    Image.network('https://images.unsplash.com/photo-1616469829581-73993eb86b02?q=80&w=1000&auto=format&fit=crop', fit: BoxFit.cover, width: double.infinity),
                    Container(color: Colors.black.withOpacity(0.3)),
                    const Icon(Icons.play_circle_outline, size: 64, color: Colors.white),
                    Positioned(
                      bottom: 16,
                      right: 16,
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(color: const Color(0xFFE50914), borderRadius: BorderRadius.circular(4)),
                        child: const Text('LIVE', style: TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold)),
                      ),
                    )
                  ],
                ),
              ),
              // EPG Section
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Evening News Live', style: TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 8),
                      const Text('18:00 - 19:30 • News & Politics', style: TextStyle(color: Color(0xFF00FF7F), fontSize: 14)),
                      const SizedBox(height: 16),
                      const Text(
                        'Join us for the latest comprehensive coverage of global events, politics, and breaking news from around the world. Expert analysis and live on-the-ground reporting.',
                        style: TextStyle(color: Colors.white70, fontSize: 14, height: 1.5),
                        maxLines: 4,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: 24),
                      const Divider(color: Colors.white12),
                      const SizedBox(height: 16),
                      const Text('Coming Up', style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 12),
                      _buildEPGItem('19:30', 'Sports Tonight', true),
                      _buildEPGItem('20:30', 'Late Night Talk Show', false),
                      _buildEPGItem('21:30', 'Documentary: The Ocean', false),
                    ],
                  ),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildEPGItem(String time, String title, bool isNext) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Row(
        children: [
          Text(time, style: TextStyle(color: isNext ? Colors.white : Colors.white54, fontWeight: isNext ? FontWeight.bold : FontWeight.normal)),
          const SizedBox(width: 16),
          Expanded(child: Text(title, style: TextStyle(color: isNext ? Colors.white : Colors.white54))),
        ],
      ),
    );
  }
}
