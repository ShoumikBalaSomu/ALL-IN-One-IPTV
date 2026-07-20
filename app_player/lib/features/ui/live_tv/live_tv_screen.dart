import 'package:flutter/material.dart';
import 'dart:ui';
import '../vod/vod_screen.dart';

class LiveTVScreen extends StatefulWidget {
  const LiveTVScreen({super.key});

  @override
  State<LiveTVScreen> createState() => _LiveTVScreenState();
}

class _LiveTVScreenState extends State<LiveTVScreen> with TickerProviderStateMixin {
  int _selectedCategoryIndex = 0;
  int _selectedChannelIndex = 0;
  bool _isSidebarExpanded = false;
  late AnimationController _pulseController;

  final List<String> _categories = ['All Channels', 'Sports', 'News', 'Movies', 'Documentaries', 'Kids', 'Music', 'International'];

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(vsync: this, duration: const Duration(seconds: 2))..repeat(reverse: true);
  }
  
  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0A0A0C),
      body: Stack(
        children: [
          // Dynamic mesh gradient background
          Positioned.fill(
            child: Container(
              decoration: BoxDecoration(
                gradient: RadialGradient(
                  center: Alignment.topLeft,
                  radius: 1.5,
                  colors: [const Color(0xFF1E2030), const Color(0xFF0A0A0C)],
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
      height: 80,
      padding: const EdgeInsets.symmetric(horizontal: 32),
      decoration: BoxDecoration(
        border: Border(bottom: BorderSide(color: Colors.white.withOpacity(0.05))),
      ),
      child: Row(
        children: [
          Text(
            _categories[_selectedCategoryIndex].toUpperCase(),
            style: const TextStyle(color: Colors.white, fontSize: 26, fontWeight: FontWeight.w900, letterSpacing: 2),
          ),
          const Spacer(),
          IconButton(icon: const Icon(Icons.sort_rounded, color: Colors.white70, size: 28), onPressed: () {}),
          const SizedBox(width: 8),
          IconButton(icon: const Icon(Icons.filter_list_rounded, color: Colors.white70, size: 28), onPressed: () {}),
          const SizedBox(width: 24),
          
          // Premium Search Bar
          Container(
            width: 250,
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.05),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.white.withOpacity(0.1)),
            ),
            child: Row(
              children: const [
                Icon(Icons.search, size: 20, color: Colors.white54),
                SizedBox(width: 12),
                Text('Search channels...', style: TextStyle(color: Colors.white30, fontSize: 14)),
              ],
            ),
          ),
          const SizedBox(width: 24),
          
          // Switch Button
          ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.white,
              foregroundColor: Colors.black,
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            ),
            icon: const Icon(Icons.movie_creation_outlined, size: 20),
            label: const Text('CINEMA MODE', style: TextStyle(fontWeight: FontWeight.w900, letterSpacing: 1)),
            onPressed: () {
              Navigator.push(context, PageRouteBuilder(
                pageBuilder: (c, a, b) => const VODScreen(),
                transitionsBuilder: (c, anim, b, child) => FadeTransition(opacity: anim, child: child),
              ));
            },
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
        duration: const Duration(milliseconds: 350),
        curve: Curves.easeOutCirc,
        width: _isSidebarExpanded ? 240 : 80,
        decoration: BoxDecoration(
          color: const Color(0xFF070709).withOpacity(0.8),
          border: Border(right: BorderSide(color: Colors.white.withOpacity(0.05))),
        ),
        child: ClipRRect(
          child: BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 30, sigmaY: 30),
            child: Column(
              children: [
                const SizedBox(height: 30),
                const Icon(Icons.tv_rounded, color: Colors.white, size: 36),
                const SizedBox(height: 50),
                Expanded(
                  child: ListView.builder(
                    physics: const BouncingScrollPhysics(),
                    itemCount: _categories.length,
                    itemBuilder: (context, index) {
                      final isSelected = index == _selectedCategoryIndex;
                      return InkWell(
                        onTap: () => setState(() => _selectedCategoryIndex = index),
                        child: Stack(
                          children: [
                            if (isSelected)
                              Positioned(
                                left: 0, top: 10, bottom: 10,
                                child: Container(width: 4, decoration: BoxDecoration(color: const Color(0xFFE50914), borderRadius: BorderRadius.circular(4))),
                              ),
                            AnimatedContainer(
                              duration: const Duration(milliseconds: 200),
                              margin: const EdgeInsets.symmetric(vertical: 4, horizontal: 12),
                              padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 16),
                              decoration: BoxDecoration(
                                color: isSelected ? Colors.white.withOpacity(0.08) : Colors.transparent,
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Row(
                                children: [
                                  Icon(
                                    _getIconForCategory(index),
                                    color: isSelected ? Colors.white : Colors.white54,
                                    size: 24,
                                  ),
                                  if (_isSidebarExpanded) ...[
                                    const SizedBox(width: 20),
                                    Expanded(
                                      child: Text(
                                        _categories[index],
                                        style: TextStyle(
                                          color: isSelected ? Colors.white : Colors.white54,
                                          fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                                          fontSize: 15,
                                        ),
                                        maxLines: 1,
                                        overflow: TextOverflow.ellipsis,
                                      ),
                                    ),
                                  ]
                                ],
                              ),
                            ),
                          ],
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
      case 0: return Icons.grid_view_rounded;
      case 1: return Icons.sports_soccer_rounded;
      case 2: return Icons.article_rounded;
      case 3: return Icons.movie_rounded;
      case 4: return Icons.public_rounded;
      case 5: return Icons.child_care_rounded;
      case 6: return Icons.music_note_rounded;
      default: return Icons.language_rounded;
    }
  }

  Widget _buildChannelList() {
    return Expanded(
      flex: 5,
      child: ListView.builder(
        padding: const EdgeInsets.all(24),
        physics: const BouncingScrollPhysics(),
        itemCount: 50,
        itemBuilder: (context, index) {
          final isSelected = index == _selectedChannelIndex;
          return Padding(
            padding: const EdgeInsets.only(bottom: 12.0),
            child: Material(
              color: Colors.transparent,
              child: InkWell(
                onTap: () => setState(() => _selectedChannelIndex = index),
                borderRadius: BorderRadius.circular(16),
                child: AnimatedContainer(
                  duration: const Duration(milliseconds: 200),
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: isSelected ? const Color(0xFF2A2D3E) : const Color(0xFF14151E),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: isSelected ? const Color(0xFF4A4E69) : Colors.transparent, width: 2),
                    boxShadow: isSelected ? [BoxShadow(color: Colors.black.withOpacity(0.3), blurRadius: 15, offset: const Offset(0, 8))] : [],
                  ),
                  child: Row(
                    children: [
                      Text('${index + 1}'.padLeft(3, '0'), style: TextStyle(color: isSelected ? Colors.white : Colors.white30, fontFamily: 'monospace', fontSize: 16, fontWeight: FontWeight.bold)),
                      const SizedBox(width: 24),
                      Container(
                        width: 60,
                        height: 60,
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(12),
                          image: DecorationImage(image: NetworkImage('https://picsum.photos/100?random=$index')),
                        ),
                      ),
                      const SizedBox(width: 24),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Network Channel ${index + 1}', style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                            const SizedBox(height: 6),
                            Row(
                              children: [
                                if (isSelected) 
                                  AnimatedBuilder(
                                    animation: _pulseController,
                                    builder: (context, child) => Container(
                                      margin: const EdgeInsets.only(right: 8),
                                      width: 8, height: 8,
                                      decoration: BoxDecoration(color: const Color(0xFFE50914).withOpacity(0.5 + (_pulseController.value * 0.5)), shape: BoxShape.circle),
                                    )
                                  ),
                                Text(
                                  isSelected ? 'LIVE: Global Evening News' : 'Up Next: Blockbuster Premiere', 
                                  style: TextStyle(color: isSelected ? Colors.white70 : Colors.white54, fontSize: 14)
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                      if (isSelected) 
                        Container(
                          padding: const EdgeInsets.all(10),
                          decoration: BoxDecoration(color: Colors.white.withOpacity(0.1), shape: BoxShape.circle),
                          child: const Icon(Icons.equalizer_rounded, color: Colors.white, size: 24)
                        ),
                    ],
                  ),
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
      flex: 4,
      child: Container(
        margin: const EdgeInsets.fromLTRB(0, 24, 32, 32),
        decoration: BoxDecoration(
          color: const Color(0xFF14151E),
          borderRadius: BorderRadius.circular(32),
          border: Border.all(color: Colors.white.withOpacity(0.05)),
          boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.8), blurRadius: 40, offset: const Offset(0, 20))],
        ),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(32),
          child: Column(
            children: [
              // Floating Video Player Simulation
              Container(
                height: 300,
                width: double.infinity,
                color: Colors.black,
                child: Stack(
                  alignment: Alignment.center,
                  children: [
                    Image.network('https://images.unsplash.com/photo-1616469829581-73993eb86b02?q=80&w=1000&auto=format&fit=crop', fit: BoxFit.cover, width: double.infinity),
                    Container(
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          begin: Alignment.topCenter, end: Alignment.bottomCenter,
                          colors: [Colors.transparent, Colors.black.withOpacity(0.8)],
                          stops: const [0.6, 1.0]
                        )
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(color: Colors.black.withOpacity(0.4), shape: BoxShape.circle, border: Border.all(color: Colors.white30)),
                      child: const Icon(Icons.play_arrow_rounded, size: 64, color: Colors.white),
                    ),
                    Positioned(
                      top: 16, right: 16,
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                        decoration: BoxDecoration(color: const Color(0xFFE50914), borderRadius: BorderRadius.circular(8)),
                        child: Row(
                          children: const [
                            Icon(Icons.circle, color: Colors.white, size: 8),
                            SizedBox(width: 6),
                            Text('LIVE', style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold, letterSpacing: 1)),
                          ],
                        ),
                      ),
                    ),
                    Positioned(
                      bottom: 0, left: 0, right: 0,
                      child: LinearProgressIndicator(value: 0.6, backgroundColor: Colors.white.withOpacity(0.2), color: const Color(0xFFE50914), minHeight: 4),
                    )
                  ],
                ),
              ),
              // EPG Section
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.all(32.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text('Global Evening News', style: TextStyle(color: Colors.white, fontSize: 28, fontWeight: FontWeight.w900)),
                                const SizedBox(height: 8),
                                const Text('18:00 - 19:30  •  News & Politics', style: TextStyle(color: Colors.white70, fontSize: 15, fontWeight: FontWeight.w500)),
                              ],
                            ),
                          ),
                          Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(color: Colors.white.withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
                            child: const Icon(Icons.info_outline_rounded, color: Colors.white),
                          )
                        ],
                      ),
                      const SizedBox(height: 24),
                      const Text(
                        'Join us for the latest comprehensive coverage of global events, politics, and breaking news from around the world. Expert analysis and live on-the-ground reporting.',
                        style: TextStyle(color: Colors.white54, fontSize: 15, height: 1.6),
                        maxLines: 4,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: 32),
                      const Text('EPG SCHEDULE', style: TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.w900, letterSpacing: 2)),
                      const SizedBox(height: 16),
                      Expanded(
                        child: ListView(
                          physics: const BouncingScrollPhysics(),
                          children: [
                            _buildEPGItem('19:30', 'Sports Tonight', 'Highlights and analysis', true),
                            _buildEPGItem('20:30', 'Late Night Talk Show', 'Celebrity interviews', false),
                            _buildEPGItem('21:30', 'Documentary: The Ocean', 'Deep sea exploration', false),
                            _buildEPGItem('23:00', 'Midnight News', 'Closing the day', false),
                          ],
                        ),
                      )
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

  Widget _buildEPGItem(String time, String title, String subtitle, bool isNext) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16.0),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isNext ? Colors.white.withOpacity(0.05) : Colors.transparent,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: isNext ? Colors.white.withOpacity(0.1) : Colors.transparent),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: isNext ? Colors.white : Colors.white.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8)
            ),
            child: Text(time, style: TextStyle(color: isNext ? Colors.black : Colors.white, fontWeight: FontWeight.bold, fontSize: 14)),
          ),
          const SizedBox(width: 20),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: TextStyle(color: isNext ? Colors.white : Colors.white70, fontWeight: FontWeight.bold, fontSize: 16)),
                const SizedBox(height: 4),
                Text(subtitle, style: const TextStyle(color: Colors.white30, fontSize: 13)),
              ],
            )
          ),
        ],
      ),
    );
  }
}
