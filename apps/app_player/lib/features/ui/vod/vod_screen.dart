import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:ui';

class VODScreen extends StatefulWidget {
  const VODScreen({super.key});

  @override
  State<VODScreen> createState() => _VODScreenState();
}

class _VODScreenState extends State<VODScreen> with SingleTickerProviderStateMixin {
  late ScrollController _scrollController;
  late AnimationController _heroAnimController;
  double _scrollOffset = 0.0;

  @override
  void initState() {
    super.initState();
    SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
    ));
    
    _scrollController = ScrollController()..addListener(() {
      setState(() { _scrollOffset = _scrollController.offset; });
    });
    
    _heroAnimController = AnimationController(vsync: this, duration: const Duration(seconds: 20))..repeat(reverse: true);
  }

  @override
  void dispose() {
    _scrollController.dispose();
    _heroAnimController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF070709),
      extendBodyBehindAppBar: true,
      appBar: _buildDynamicAppBar(),
      body: SingleChildScrollView(
        controller: _scrollController,
        physics: const BouncingScrollPhysics(),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildAnimatedHero(),
            Transform.translate(
              offset: const Offset(0, -40),
              child: Column(
                children: [
                  _buildCategoryRow('Trending Now', true),
                  _buildCategoryRow('Top 10 in Your Country', false, isTop10: true),
                  _buildCategoryRow('Action & Adventure', false),
                  _buildCategoryRow('Sci-Fi Masterpieces', false),
                  const SizedBox(height: 100),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  PreferredSizeWidget _buildDynamicAppBar() {
    final blurAmount = (_scrollOffset / 10).clamp(0.0, 20.0);
    final bgOpacity = (_scrollOffset / 200).clamp(0.0, 0.85);

    return PreferredSize(
      preferredSize: const Size.fromHeight(80),
      child: ClipRRect(
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: blurAmount, sigmaY: blurAmount),
          child: Container(
            color: const Color(0xFF070709).withValues(alpha: bgOpacity),
            padding: const EdgeInsets.only(top: 40, left: 24, right: 24, bottom: 10),
            child: Row(
              children: [
                const Text('CINEMA', style: TextStyle(color: Color(0xFFE50914), fontWeight: FontWeight.w900, fontSize: 28, letterSpacing: 3)),
                const Spacer(),
                Icon(Icons.cast, color: Colors.white.withValues(alpha: 0.8), size: 28),
                const SizedBox(width: 20),
                Icon(Icons.search, color: Colors.white.withValues(alpha: 0.8), size: 28),
                const SizedBox(width: 20),
                Container(
                  width: 36, height: 36,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(color: const Color(0xFFE50914), width: 2),
                    image: const DecorationImage(image: NetworkImage('https://i.pravatar.cc/150?img=11')),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildAnimatedHero() {
    return SizedBox(
      height: 520,
      width: double.infinity,
      child: Stack(
        children: [
          Positioned.fill(
            child: Image.network(
              'https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=1000',
              fit: BoxFit.cover,
            ),
          ),
          Positioned.fill(
            child: Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    Colors.transparent,
                    const Color(0xFF070709).withValues(alpha: 0.5),
                    const Color(0xFF070709),
                  ],
                ),
              ),
            ),
          ),
          Positioned(
            left: 24, right: 24, bottom: 60,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: const Color(0xFFE50914),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: const Text('TOP 10', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12)),
                    ),
                    const SizedBox(width: 10),
                    const Text('#1 in Movies Today', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w600, fontSize: 14)),
                  ],
                ),
                const SizedBox(height: 12),
                const Text('CYBERPUNK 2088', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 40, letterSpacing: 2)),
                const SizedBox(height: 12),
                Row(
                  children: [
                    ElevatedButton.icon(
                      onPressed: () {},
                      icon: const Icon(Icons.play_arrow, color: Colors.black, size: 28),
                      label: const Text('Play', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold, fontSize: 16)),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 14),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                      ),
                    ),
                    const SizedBox(width: 16),
                    OutlinedButton.icon(
                      onPressed: () {},
                      icon: const Icon(Icons.add, color: Colors.white, size: 24),
                      label: const Text('My List', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
                      style: OutlinedButton.styleFrom(
                        side: const BorderSide(color: Colors.white, width: 2),
                        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCategoryRow(String title, bool isHeroRow, {bool isTop10 = false}) {
    return Padding(
      padding: const EdgeInsets.only(left: 24, bottom: 24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 20, letterSpacing: 0.5)),
          const SizedBox(height: 12),
          SizedBox(
            height: isTop10 ? 200 : 160,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              physics: const BouncingScrollPhysics(),
              itemCount: 10,
              itemBuilder: (context, index) {
                return Container(
                  width: isTop10 ? 140 : 110,
                  margin: const EdgeInsets.only(right: 12),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(12),
                    image: DecorationImage(
                      image: NetworkImage('https://picsum.photos/seed/${title.hashCode + index}/300/450'),
                      fit: BoxFit.cover,
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: 0.4),
                        blurRadius: 10,
                        offset: const Offset(0, 4),
                      ),
                    ],
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
