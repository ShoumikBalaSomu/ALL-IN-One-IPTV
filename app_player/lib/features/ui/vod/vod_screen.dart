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
        preferredSize: const Size.fromHeight(70),
        child: ClipRRect(
          child: BackdropFilter(
            filter: ImageFilter.blur(
              sigmaX: _scrollOffset > 50 ? 15.0 : 0.0,
              sigmaY: _scrollOffset > 50 ? 15.0 : 0.0,
            ),
            child: AppBar(
              backgroundColor: _scrollOffset > 50 ? Colors.black.withOpacity(0.6) : Colors.transparent,
              elevation: 0,
              title: Row(
                children: [
                  const Text('CINEMA', style: TextStyle(color: Color(0xFFE50914), fontWeight: FontWeight.w900, fontSize: 24, letterSpacing: 2)),
                  const Spacer(),
                  IconButton(icon: const Icon(Icons.cast, color: Colors.white), onPressed: () {}),
                  IconButton(icon: const Icon(Icons.search, color: Colors.white), onPressed: () {}),
                  const CircleAvatar(
                    radius: 16,
                    backgroundImage: NetworkImage('https://i.pravatar.cc/150?img=11'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
      body: SingleChildScrollView(
        controller: _scrollController,
        physics: const BouncingScrollPhysics(),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildHeroBanner(),
            const SizedBox(height: 20),
            _buildCategoryRow('Trending Now', true),
            _buildCategoryRow('Top 10 in Your Country', false, isTop10: true),
            _buildCategoryRow('Action & Adventure', false),
            _buildCategoryRow('Sci-Fi Masterpieces', false),
            const SizedBox(height: 100), // padding for bottom nav if any
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
          width: double.infinity,
          decoration: const BoxDecoration(
            image: DecorationImage(
              image: NetworkImage('https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=2000&auto=format&fit=crop'),
              fit: BoxFit.cover,
            ),
          ),
        ),
        // Gradient overlay for bottom fade
        Container(
          height: 550,
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [
                Colors.black.withOpacity(0.4),
                Colors.transparent,
                const Color(0xFF0F1014).withOpacity(0.8),
                const Color(0xFF0F1014),
              ],
              stops: const [0.0, 0.3, 0.8, 1.0],
            ),
          ),
        ),
        Positioned(
          bottom: 40,
          left: 0,
          right: 0,
          child: Column(
            children: [
              const Text(
                'INTERSTELLAR',
                style: TextStyle(fontSize: 48, fontWeight: FontWeight.w900, color: Colors.white, letterSpacing: 4, shadows: [BoxShadow(color: Colors.black, blurRadius: 20)]),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  Text('Sci-Fi', style: TextStyle(color: Colors.white70, fontSize: 14)),
                  Padding(padding: EdgeInsets.symmetric(horizontal: 8.0), child: Icon(Icons.circle, size: 6, color: Colors.white30)),
                  Text('2014', style: TextStyle(color: Colors.white70, fontSize: 14)),
                  Padding(padding: EdgeInsets.symmetric(horizontal: 8.0), child: Icon(Icons.circle, size: 6, color: Colors.white30)),
                  Text('4K HDR', style: TextStyle(color: Color(0xFFE50914), fontSize: 14, fontWeight: FontWeight.bold)),
                ],
              ),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white,
                      foregroundColor: Colors.black,
                      padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 12),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                    ),
                    icon: const Icon(Icons.play_arrow, size: 28),
                    label: const Text('Play', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                    onPressed: () {},
                  ),
                  const SizedBox(width: 16),
                  ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white.withOpacity(0.2),
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                    ),
                    icon: const Icon(Icons.add, size: 28),
                    label: const Text('My List', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                    onPressed: () {},
                  ),
                ],
              )
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildCategoryRow(String title, bool isLarge, {bool isTop10 = false}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
          child: Text(title, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
        ),
        SizedBox(
          height: isLarge ? 220 : 160,
          child: ListView.builder(
            padding: const EdgeInsets.symmetric(horizontal: 12),
            scrollDirection: Axis.horizontal,
            physics: const BouncingScrollPhysics(),
            itemCount: 10,
            itemBuilder: (context, index) {
              return Stack(
                alignment: Alignment.bottomLeft,
                children: [
                  Container(
                    width: isLarge ? 140 : 110,
                    margin: const EdgeInsets.symmetric(horizontal: 4),
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(8),
                      color: Colors.grey[900],
                      image: DecorationImage(
                        image: NetworkImage('https://picsum.photos/300/450?random=${title.hashCode + index}'),
                        fit: BoxFit.cover,
                      ),
                    ),
                  ),
                  if (isTop10)
                    Positioned(
                      left: -10,
                      bottom: -20,
                      child: Text(
                        '${index + 1}',
                        style: TextStyle(
                          fontSize: 100,
                          fontWeight: FontWeight.w900,
                          color: Colors.black,
                          foreground: Paint()
                            ..style = PaintingStyle.stroke
                            ..strokeWidth = 2
                            ..color = Colors.white,
                        ),
                      ),
                    ),
                ],
              );
            },
          ),
        ),
      ],
    );
  }
}
