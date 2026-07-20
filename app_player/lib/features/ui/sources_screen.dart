import 'package:flutter/material.dart';
import 'dart:ui';
import 'live_tv/live_tv_screen.dart';

class SourcesScreen extends StatefulWidget {
  const SourcesScreen({super.key});

  @override
  State<SourcesScreen> createState() => _SourcesScreenState();
}

class _SourcesScreenState extends State<SourcesScreen> with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: const Duration(milliseconds: 1500))..forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          // Background Gradient Orbs
          Positioned(
            top: -100,
            left: -100,
            child: Container(
              width: 300,
              height: 300,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: const Color(0xFFE50914).withOpacity(0.3),
                boxShadow: const [BoxShadow(color: Color(0xFFE50914), blurRadius: 100, spreadRadius: 100)],
              ),
            ),
          ),
          Positioned(
            bottom: -50,
            right: -100,
            child: Container(
              width: 250,
              height: 250,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: const Color(0xFF00C6FF).withOpacity(0.2),
                boxShadow: const [BoxShadow(color: Color(0xFF00C6FF), blurRadius: 100, spreadRadius: 100)],
              ),
            ),
          ),
          // Glassmorphism Content
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 40),
                  FadeTransition(
                    opacity: Tween<double>(begin: 0, end: 1).animate(CurvedAnimation(parent: _controller, curve: const Interval(0.0, 0.4, curve: Curves.easeOut))),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: const [
                        Text('Welcome to', style: TextStyle(color: Colors.white70, fontSize: 18, letterSpacing: 1.5)),
                        SizedBox(height: 8),
                        Text('ALL-IN-ONE', style: TextStyle(color: Colors.white, fontSize: 42, fontWeight: FontWeight.w900, letterSpacing: 2)),
                        Text('IPTV', style: TextStyle(color: Color(0xFFE50914), fontSize: 42, fontWeight: FontWeight.w900, letterSpacing: 2)),
                        SizedBox(height: 12),
                        Text('Select your premium media provider to begin streaming.', style: TextStyle(color: Colors.white54, fontSize: 14)),
                      ],
                    ),
                  ),
                  const SizedBox(height: 40),
                  Expanded(
                    child: ListView(
                      physics: const BouncingScrollPhysics(),
                      children: [
                        _buildAnimatedCard(0, 'M3U URL / Playlist', 'Standard IPTV playlist URL', Icons.link, const Color(0xFFE50914)),
                        _buildAnimatedCard(1, 'Xtream Codes', 'Login with API credentials', Icons.tv, const Color(0xFF00C6FF)),
                        _buildAnimatedCard(2, 'MAC Portal (Stalker)', 'Connect using MAC address', Icons.settings_ethernet, const Color(0xFF8A2BE2)),
                        _buildAnimatedCard(3, 'Emby / Jellyfin', 'Personal media server', Icons.dns, const Color(0xFF00FF7F)),
                        _buildAnimatedCard(4, 'Plex', 'Login with Plex account', Icons.play_circle_filled, const Color(0xFFFFA500)),
                      ],
                    ),
                  ),
                  FadeTransition(
                    opacity: Tween<double>(begin: 0, end: 1).animate(CurvedAnimation(parent: _controller, curve: const Interval(0.8, 1.0, curve: Curves.easeOut))),
                    child: Padding(
                      padding: const EdgeInsets.only(bottom: 24.0, top: 16.0),
                      child: Container(
                        width: double.infinity,
                        height: 60,
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(16),
                          gradient: const LinearGradient(colors: [Color(0xFFE50914), Color(0xFF8A0000)]),
                          boxShadow: [BoxShadow(color: const Color(0xFFE50914).withOpacity(0.5), blurRadius: 20, offset: const Offset(0, 10))],
                        ),
                        child: ElevatedButton(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.transparent,
                            shadowColor: Colors.transparent,
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                          ),
                          onPressed: () {
                            Navigator.pushReplacement(context, PageRouteBuilder(
                              pageBuilder: (context, animation, secondaryAnimation) => const LiveTVScreen(),
                              transitionsBuilder: (context, animation, secondaryAnimation, child) {
                                return FadeTransition(opacity: animation, child: child);
                              },
                            ));
                          },
                          child: const Text('CONTINUE AS GUEST', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white, letterSpacing: 1.2)),
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

  Widget _buildAnimatedCard(int index, String title, String subtitle, IconData icon, Color glowColor) {
    final delay = 0.2 + (index * 0.1);
    final slideAnim = Tween<Offset>(begin: const Offset(0, 0.5), end: Offset.zero).animate(
      CurvedAnimation(parent: _controller, curve: Interval(delay, delay + 0.4, curve: Curves.easeOutCubic)),
    );
    final fadeAnim = Tween<double>(begin: 0, end: 1).animate(
      CurvedAnimation(parent: _controller, curve: Interval(delay, delay + 0.4, curve: Curves.easeOut)),
    );

    return SlideTransition(
      position: slideAnim,
      child: FadeTransition(
        opacity: fadeAnim,
        child: Padding(
          padding: const EdgeInsets.only(bottom: 16.0),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(20),
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.05),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: Colors.white.withOpacity(0.1)),
                ),
                child: Material(
                  color: Colors.transparent,
                  child: InkWell(
                    borderRadius: BorderRadius.circular(20),
                    highlightColor: glowColor.withOpacity(0.2),
                    splashColor: glowColor.withOpacity(0.3),
                    onTap: () {
                      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                        content: Text('Configuring $title...'),
                        backgroundColor: glowColor,
                        behavior: SnackBarBehavior.floating,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                      ));
                    },
                    child: Padding(
                      padding: const EdgeInsets.all(20.0),
                      child: Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: glowColor.withOpacity(0.2),
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(color: glowColor.withOpacity(0.5)),
                            ),
                            child: Icon(icon, size: 28, color: glowColor),
                          ),
                          const SizedBox(width: 20),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Colors.white)),
                                const SizedBox(height: 4),
                                Text(subtitle, style: const TextStyle(color: Colors.white54, fontSize: 13)),
                              ],
                            ),
                          ),
                          Icon(Icons.arrow_forward_ios, size: 16, color: Colors.white.withOpacity(0.3)),
                        ],
                      ),
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
