import 'package:flutter/material.dart';
import 'dart:ui';

class VODScreen extends StatefulWidget {
  const VODScreen({super.key});

  @override
  State<VODScreen> createState() => _VODScreenState();
}

class _VODScreenState extends State<VODScreen> {
  final ScrollController _scrollController = ScrollController();
  double _scrollOffset = 0.0;

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(() {
      setState(() {
        _scrollOffset = _scrollController.offset;
      });
    });
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F1014),
      extendBodyBehindAppBar: true,
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(70.0),
        child: ClipRRect(
          child: BackdropFilter(
            filter: ImageFilter.blur(sigmaX: _scrollOffset > 50 ? 10 : 0, sigmaY: _scrollOffset > 50 ? 10 : 0),
            child: AppBar(
              backgroundColor: const Color(0xFF0F1014).withOpacity((_scrollOffset / 350).clamp(0, 0.85).toDouble()),
              elevation: 0,
              title: const Text('ALL-IN-One IPTV', style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold, fontSize: 24)),
              actions: [
                IconButton(icon: const Icon(Icons.search, color: Colors.white), onPressed: () {}),
                IconButton(icon: const Icon(Icons.person, color: Colors.white), onPressed: () {}),
              ],
            ),
          ),
        ),
      ),
      body: SingleChildScrollView(
        controller: _scrollController,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildHeroBanner(),
            const SizedBox(height: 20),
            _buildCategoryCarousel('Trending Now'),
            _buildCategoryCarousel('Action & Adventure'),
            _buildCategoryCarousel('Comedies'),
            _buildCategoryCarousel('Sci-Fi'),
            const SizedBox(height: 40),
          ],
        ),
      ),
    );
  }

  Widget _buildHeroBanner() {
    return Stack(
      children: [
        Container(
          height: 550,
          decoration: const BoxDecoration(
            image: DecorationImage(
              image: NetworkImage('https://images.unsplash.com/photo-1536440136628-849c177e76a1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80'),
              fit: BoxFit.cover,
            ),
          ),
        ),
        Container(
          height: 550,
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [
                const Color(0xFF0F1014).withOpacity(1.0),
                const Color(0xFF0F1014).withOpacity(0.0),
              ],
              begin: Alignment.bottomCenter,
              end: Alignment.topCenter,
              stops: const [0.0, 0.5],
            ),
          ),
        ),
        Positioned(
          bottom: 40,
          left: 20,
          right: 20,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('The Grand Aggregator', style: TextStyle(color: Colors.white, fontSize: 40, fontWeight: FontWeight.w900, shadows: [Shadow(color: Colors.black, blurRadius: 10)])),
              const SizedBox(height: 10),
              const Text('Experience the ultimate combination of all your favorite streams and playlists in one unified interface. No dead links. No duplicates.', style: TextStyle(color: Colors.white70, fontSize: 16)),
              const SizedBox(height: 20),
              Row(
                children: [
                  ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white,
                      foregroundColor: Colors.black,
                      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
                    ),
                    icon: const Icon(Icons.play_arrow, size: 28),
                    label: const Text('Play', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                    onPressed: () {},
                  ),
                  const SizedBox(width: 15),
                  ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white.withOpacity(0.2),
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
                    ),
                    icon: const Icon(Icons.info_outline, size: 28),
                    label: const Text('More Info', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                    onPressed: () {},
                  ),
                ],
              )
            ],
          ),
        )
      ],
    );
  }

  Widget _buildCategoryCarousel(String title) {
    return Padding(
      padding: const EdgeInsets.only(left: 20.0, bottom: 20.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          SizedBox(
            height: 200,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              itemCount: 10,
              itemBuilder: (context, index) {
                return Container(
                  width: 130,
                  margin: const EdgeInsets.only(right: 12),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(8),
                    gradient: const LinearGradient(
                      colors: [Color(0xFF1E1E24), Color(0xFF2A2A35)],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    boxShadow: [
                      BoxShadow(color: Colors.black.withOpacity(0.5), blurRadius: 5, offset: const Offset(2, 4))
                    ]
                  ),
                  child: Material(
                    color: Colors.transparent,
                    child: InkWell(
                      borderRadius: BorderRadius.circular(8),
                      onTap: () {},
                      child: Center(
                        child: Text('Movie ${index + 1}', style: const TextStyle(color: Colors.white54, fontWeight: FontWeight.bold)),
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
