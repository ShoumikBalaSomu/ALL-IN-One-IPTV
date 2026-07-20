import 'package:flutter/material.dart';
import 'dart:ui';
import 'dart:math' as math;
import 'live_tv/live_tv_screen.dart';

class SourcesScreen extends StatefulWidget {
  const SourcesScreen({super.key});

  @override
  State<SourcesScreen> createState() => _SourcesScreenState();
}

class _SourcesScreenState extends State<SourcesScreen> with TickerProviderStateMixin {
  late AnimationController _fadeController;
  late AnimationController _particleController;

  @override
  void initState() {
    super.initState();
    _fadeController = AnimationController(vsync: this, duration: const Duration(milliseconds: 2000))..forward();
    _particleController = AnimationController(vsync: this, duration: const Duration(seconds: 10))..repeat();
  }

  @override
  void dispose() {
    _fadeController.dispose();
    _particleController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF070709),
      body: Stack(
        children: [
          // Deep Space Animated Background
          Positioned.fill(
            child: AnimatedBuilder(
              animation: _particleController,
              builder: (context, child) {
                return CustomPaint(painter: ParticlePainter(_particleController.value));
              },
            ),
          ),
          // Glow Orbs
          Positioned(top: -150, left: -100, child: _buildGlowOrb(const Color(0xFFE50914), 400)),
          Positioned(bottom: -150, right: -100, child: _buildGlowOrb(const Color(0xFF00C6FF), 400)),

          SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 60),
                  FadeTransition(
                    opacity: Tween<double>(begin: 0, end: 1).animate(CurvedAnimation(parent: _fadeController, curve: const Interval(0.0, 0.4, curve: Curves.easeOut))),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('NEXUS', style: TextStyle(color: Colors.white.withOpacity(0.5), fontSize: 16, letterSpacing: 4, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 4),
                        ShaderMask(
                          shaderCallback: (bounds) => const LinearGradient(colors: [Colors.white, Color(0xFFAAAAAA)]).createShader(bounds),
                          child: const Text('STREAMING', style: TextStyle(color: Colors.white, fontSize: 48, fontWeight: FontWeight.w900, letterSpacing: -1)),
                        ),
                        const Text('HUB', style: TextStyle(color: Color(0xFFE50914), fontSize: 48, fontWeight: FontWeight.w900, letterSpacing: -1, height: 0.9)),
                        const SizedBox(height: 16),
                        const Text('Connect your media sources to initialize the ultra-premium viewing experience.', style: TextStyle(color: Colors.white54, fontSize: 15, height: 1.4)),
                      ],
                    ),
                  ),
                  const SizedBox(height: 50),
                  Expanded(
                    child: ListView(
                      physics: const BouncingScrollPhysics(),
                      children: [
                        _buildSourceCard(0, 'M3U URL / Playlist', 'Standard IPTV playlist URL', Icons.link, const Color(0xFFE50914)),
                        _buildSourceCard(1, 'Xtream Codes', 'Login with API credentials', Icons.tv, const Color(0xFF00C6FF)),
                        _buildSourceCard(2, 'MAC Portal', 'Connect using MAC address', Icons.settings_ethernet, const Color(0xFF8A2BE2)),
                        _buildSourceCard(3, 'Emby / Jellyfin', 'Personal media server', Icons.dns, const Color(0xFF00FF7F)),
                        _buildSourceCard(4, 'Plex', 'Login with Plex account', Icons.play_circle_filled, const Color(0xFFFFA500)),
                        const SizedBox(height: 40),
                      ],
                    ),
                  ),
                  
                  // Guest Login Button
                  FadeTransition(
                    opacity: Tween<double>(begin: 0, end: 1).animate(CurvedAnimation(parent: _fadeController, curve: const Interval(0.7, 1.0, curve: Curves.easeOut))),
                    child: Padding(
                      padding: const EdgeInsets.only(bottom: 24.0),
                      child: InkWell(
                        onTap: () => Navigator.pushReplacement(context, PageRouteBuilder(
                          pageBuilder: (c, a, s) => const LiveTVScreen(),
                          transitionsBuilder: (c, a, s, child) => FadeTransition(opacity: a, child: child),
                          transitionDuration: const Duration(milliseconds: 800)
                        )),
                        child: Container(
                          width: double.infinity,
                          height: 65,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(20),
                            gradient: const LinearGradient(colors: [Color(0xFFE50914), Color(0xFF8A0000)]),
                            boxShadow: [BoxShadow(color: const Color(0xFFE50914).withOpacity(0.4), blurRadius: 20, offset: const Offset(0, 10))],
                          ),
                          alignment: Alignment.Center,
                          child: const Text('ENTER AS GUEST', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w900, color: Colors.white, letterSpacing: 2)),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildGlowOrb(Color color, double size) {
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: color.withOpacity(0.15),
        boxShadow: [BoxShadow(color: color.withOpacity(0.3), blurRadius: size / 2, spreadRadius: size / 2)],
      ),
    );
  }

  Widget _buildSourceCard(int index, String title, String subtitle, IconData icon, Color accentColor) {
    final delay = 0.3 + (index * 0.1);
    final anim = CurvedAnimation(parent: _fadeController, curve: Interval(delay, delay + 0.4, curve: Curves.easeOutCubic));

    return SlideTransition(
      position: Tween<Offset>(begin: const Offset(0, 0.3), end: Offset.zero).animate(anim),
      child: FadeTransition(
        opacity: Tween<double>(begin: 0, end: 1).animate(anim),
        child: Container(
          margin: const EdgeInsets.only(bottom: 16.0),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(24),
            color: Colors.white.withOpacity(0.03),
            border: Border.all(color: Colors.white.withOpacity(0.08)),
            boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.2), blurRadius: 10, offset: const Offset(0, 5))],
          ),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(24),
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 15, sigmaY: 15),
              child: Material(
                color: Colors.transparent,
                child: InkWell(
                  onTap: () {},
                  highlightColor: accentColor.withOpacity(0.1),
                  splashColor: accentColor.withOpacity(0.2),
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.all(14),
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            gradient: LinearGradient(
                              colors: [accentColor.withOpacity(0.2), accentColor.withOpacity(0.05)],
                              begin: Alignment.topLeft, end: Alignment.bottomRight,
                            ),
                            border: Border.all(color: accentColor.withOpacity(0.5)),
                          ),
                          child: Icon(icon, size: 28, color: accentColor),
                        ),
                        const SizedBox(width: 20),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Colors.white)),
                              const SizedBox(height: 4),
                              Text(subtitle, style: TextStyle(color: Colors.white.withOpacity(0.5), fontSize: 13)),
                            ],
                          ),
                        ),
                        Icon(Icons.arrow_forward_ios, size: 16, color: Colors.white.withOpacity(0.2)),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class ParticlePainter extends CustomPainter {
  final double progress;
  ParticlePainter(this.progress);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..color = Colors.white.withOpacity(0.3)..style = PaintingStyle.fill;
    final random = math.Random(42); // fixed seed for consistent positions

    for (int i = 0; i < 50; i++) {
      final xBase = random.nextDouble() * size.width;
      final yBase = random.nextDouble() * size.height;
      final speed = 0.5 + random.nextDouble() * 2;
      
      // Calculate vertical drift
      double y = (yBase - (progress * size.height * speed)) % size.height;
      if (y < 0) y += size.height;
      
      // Calculate horizontal wobble
      final x = xBase + math.sin((progress * math.pi * 2) + i) * 10;
      
      final radius = 0.5 + random.nextDouble() * 1.5;
      
      // Twinkle effect
      paint.color = Colors.white.withOpacity( (math.sin(progress * math.pi * 4 + i) + 1) / 2 * 0.5 );
      canvas.drawCircle(Offset(x, y), radius, paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
