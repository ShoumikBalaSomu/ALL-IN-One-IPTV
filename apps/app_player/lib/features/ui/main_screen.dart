import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'live_tv/live_tv_screen.dart';
import 'vod/vod_screen.dart';

final navIndexProvider = StateProvider<int>((ref) => 0);

class MainScreen extends ConsumerWidget {
  const MainScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final currentIndex = ref.watch(navIndexProvider);
    final isDesktop = MediaQuery.of(context).size.width > 800;

    final screens = [
      const LiveTVScreen(),
      const VODScreen(),
    ];

    return Scaffold(
      extendBody: true, // Allow content behind bottom nav
      body: Stack(
        children: [
          // Dynamic Mesh/Gradient Background Base
          Container(
            decoration: const BoxDecoration(
              gradient: RadialGradient(
                center: Alignment(-0.8, -0.6),
                radius: 1.5,
                colors: [
                  Color(0xFF1E1B4B), // Deep Indigo
                  Color(0xFF0F172A), // Slate 900
                  Color(0xFF020617), // Slate 950
                ],
              ),
            ),
          ),
          
          // Main Content Area
          Row(
            children: [
              if (isDesktop) _buildGlassSideRail(context, ref, currentIndex),
              Expanded(
                child: AnimatedSwitcher(
                  duration: const Duration(milliseconds: 400),
                  switchInCurve: Curves.easeOutCubic,
                  switchOutCurve: Curves.easeInCubic,
                  transitionBuilder: (child, animation) {
                    return FadeTransition(
                      opacity: animation,
                      child: SlideTransition(
                        position: Tween<Offset>(
                          begin: const Offset(0.05, 0),
                          end: Offset.zero,
                        ).animate(animation),
                        child: child,
                      ),
                    );
                  },
                  child: screens[currentIndex],
                ),
              ),
            ],
          ),
          
          // Mobile Floating Bottom Nav
          if (!isDesktop)
            Align(
              alignment: Alignment.bottomCenter,
              child: _buildGlassBottomNav(context, ref, currentIndex),
            ),
        ],
      ),
    );
  }

  Widget _buildGlassBottomNav(BuildContext context, WidgetRef ref, int currentIndex) {
    return Container(
      margin: const EdgeInsets.only(left: 24, right: 24, bottom: 24),
      height: 70,
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.05),
        borderRadius: BorderRadius.circular(35),
        border: Border.all(color: Colors.white.withValues(alpha: 0.1), width: 1.5),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.3),
            blurRadius: 20,
            spreadRadius: 5,
          )
        ],
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(35),
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 15, sigmaY: 15),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              _buildNavItem(context, ref, 0, currentIndex, Icons.tv, 'Live TV'),
              _buildNavItem(context, ref, 1, currentIndex, Icons.movie_filter, 'Movies'),
            ],
          ),
        ),
      ),
    ).animate().slideY(begin: 1, end: 0, duration: 600.ms, curve: Curves.easeOutBack);
  }

  Widget _buildGlassSideRail(BuildContext context, WidgetRef ref, int currentIndex) {
    return Container(
      width: 100,
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.03),
        border: Border(
          right: BorderSide(color: Colors.white.withValues(alpha: 0.05), width: 1),
        ),
      ),
      child: ClipRRect(
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 20, sigmaY: 20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _buildNavItem(context, ref, 0, currentIndex, Icons.tv, 'Live TV', isVertical: true),
              const SizedBox(height: 40),
              _buildNavItem(context, ref, 1, currentIndex, Icons.movie_filter, 'Movies', isVertical: true),
            ],
          ),
        ),
      ),
    ).animate().slideX(begin: -1, end: 0, duration: 600.ms, curve: Curves.easeOutBack);
  }

  Widget _buildNavItem(BuildContext context, WidgetRef ref, int index, int currentIndex, IconData icon, String label, {bool isVertical = false}) {
    final isSelected = currentIndex == index;
    final primaryColor = Theme.of(context).colorScheme.primary;

    return GestureDetector(
      onTap: () => ref.read(navIndexProvider.notifier).state = index,
      behavior: HitTestBehavior.opaque,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOutCubic,
        padding: EdgeInsets.symmetric(horizontal: isVertical ? 0 : 20, vertical: 12),
        decoration: BoxDecoration(
          color: isSelected ? primaryColor.withValues(alpha: 0.15) : Colors.transparent,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(
            color: isSelected ? primaryColor.withValues(alpha: 0.5) : Colors.transparent,
            width: 1,
          ),
        ),
        child: Flex(
          direction: isVertical ? Axis.vertical : Axis.horizontal,
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              color: isSelected ? primaryColor : Colors.white54,
              size: 28,
            ),
            if (!isVertical || isSelected) ...[
              SizedBox(width: isVertical ? 0 : 8, height: isVertical ? 8 : 0),
              Text(
                label,
                style: TextStyle(
                  color: isSelected ? primaryColor : Colors.white54,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                  fontSize: 14,
                ),
              ),
            ]
          ],
        ),
      ),
    );
  }
}
