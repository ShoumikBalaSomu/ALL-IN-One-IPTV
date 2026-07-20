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
    // Configure system UI for immersive experience
    SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(statusBarColor: Colors.transparent, statusBarIconBrightness: Brightness.light));
    
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
      bottomNavigationBar: _buildBottomNav(),
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
            color: Color(0xFF070709).withOpacity(bgOpacity),
            padding: const EdgeInsets.only(top: 40, left: 24, right: 24, bottom: 10),
            child: Row(
              children: [
                const Text('CINEMA', style: TextStyle(color: Color(0xFFE50914), fontWeight: FontWeight.w900, fontSize: 28, letterSpacing: 3)),
                const Spacer(),
                Icon(Icons.cast, color: Colors.white.withOpacity(0.8), size: 28),
                const SizedBox(width: 20),
                Icon(Icons.search, color: Colors.white.withOpacity(0.8), size: 28),
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
      height: 600,
      width: double.infinity,
      child: Stack(
        fit: StackFit.expand,
        children: [
          // Slowly zooming background image
          AnimatedBuilder(
            animation: _heroAnimController,
            builder: (context, child) {
              return Transform.scale(
                scale: 1.0 + (_heroAnimController.value * 0.1),
                child: Image.network(
                  'https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=2000&auto=format&fit=crop',
                  fit: BoxFit.cover,
                  color: Colors.black.withOpacity(0.2), // slight darken
                  colorBlendMode: BlendMode.darken,
                ),
              );
            }
          ),
          // Complex fading gradient
          Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  const Color(0xFF070709).withOpacity(0.6),
                  Colors.transparent,
                  const Color(0xFF070709).withOpacity(0.5),
                  const Color(0xFF070709).withOpacity(0.9),
                  const Color(0xFF070709),
                ],
                stops: const [0.0, 0.2, 0.6, 0.85, 1.0],
              ),
            ),
          ),
          // Hero Content
          Positioned(
            bottom: 60,
            left: 0,
            right: 0,
            child: Column(
              children: [
                Image.network('https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Interstellar_logo.svg/1200px-Interstellar_logo.svg.png', width: 250, color: Colors.white),
                const SizedBox(height: 20),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text('Sci-Fi', style: TextStyle(color: Colors.white70, fontSize: 13, fontWeight: FontWeight.w600)),
                    const Padding(padding: EdgeInsets.symmetric(horizontal: 10.0), child: Icon(Icons.circle, size: 5, color: Colors.white30)),
                    const Text('2014', style: TextStyle(color: Colors.white70, fontSize: 13, fontWeight: FontWeight.w600)),
                    const Padding(padding: EdgeInsets.symmetric(horizontal: 10.0), child: Icon(Icons.circle, size: 5, color: Colors.white30)),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                      decoration: BoxDecoration(border: Border.all(color: Colors.white54), borderRadius: BorderRadius.circular(4)),
                      child: const Text('4K HDR', style: TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold)),
                    ),
                  ],
                ),
                const SizedBox(height: 24),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    _buildHeroButton(Icons.play_arrow_rounded, 'Play', Colors.white, Colors.black),
                    const SizedBox(width: 16),
                    _buildHeroButton(Icons.add, 'My List', Colors.white.withOpacity(0.2), Colors.white),
                  ],
                )
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHeroButton(IconData icon, String label, Color bgColor, Color textColor) {
    return Material(
      color: bgColor,
      borderRadius: BorderRadius.circular(12),
      child: InkWell(
        onTap: () {},
        borderRadius: BorderRadius.circular(12),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 14),
          child: Row(
            children: [
              Icon(icon, size: 26, color: textColor),
              const SizedBox(width: 8),
              Text(label, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: textColor)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildCategoryRow(String title, bool isLarge, {bool isTop10 = false}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 20.0, bottom: 12.0, top: 24.0),
          child: Text(title, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white, letterSpacing: -0.5)),
        ),
        SizedBox(
          height: isLarge ? 240 : 180,
          child: ListView.builder(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            scrollDirection: Axis.horizontal,
            physics: const BouncingScrollPhysics(),
            itemCount: 10,
            itemBuilder: (context, index) {
              return Container(
                width: isLarge ? 160 : 120,
                margin: const EdgeInsets.only(right: 12),
                child: Stack(
                  clipBehavior: Clip.none,
                  children: [
                    // Movie Poster with scale on hover/press simulation
                    Positioned.fill(
                      child: Material(
                        color: Colors.transparent,
                        child: InkWell(
                          onTap: () {},
                          borderRadius: BorderRadius.circular(12),
                          child: Container(
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(12),
                              color: const Color(0xFF1E1E24),
                              image: DecorationImage(
                                image: NetworkImage('https://picsum.photos/300/450?random=${title.hashCode + index}'),
                                fit: BoxFit.cover,
                              ),
                              boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.5), blurRadius: 10, offset: const Offset(0, 5))],
                            ),
                          ),
                        ),
                      ),
                    ),
                    if (isTop10)
                      Positioned(
                        left: -15,
                        bottom: -25,
                        child: Stack(
                          children: [
                            Text(
                              '${index + 1}',
                              style: TextStyle(
                                fontSize: 130,
                                fontWeight: FontWeight.w900,
                                letterSpacing: -10,
                                foreground: Paint()..style = PaintingStyle.stroke..strokeWidth = 6..color = Colors.black,
                              ),
                            ),
                            Text(
                              '${index + 1}',
                              style: const TextStyle(
                                fontSize: 130,
                                fontWeight: FontWeight.w900,
                                color: Colors.white,
                                letterSpacing: -10,
                              ),
                            ),
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
    );
  }

  Widget _buildBottomNav() {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.bottomCenter,
          end: Alignment.topCenter,
          colors: [Colors.black, Colors.black.withOpacity(0.9), Colors.transparent],
        ),
      ),
      child: BottomNavigationBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        selectedItemColor: Colors.white,
        unselectedItemColor: Colors.white54,
        type: BottomNavigationBarType.fixed,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home_filled), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.play_circle_outline), label: 'New & Hot'),
          BottomNavigationBarItem(icon: Icon(Icons.account_circle_outlined), label: 'My Space'),
        ],
      ),
    );
  }
}
