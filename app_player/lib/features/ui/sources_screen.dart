import 'package:flutter/material.dart';
import 'live_tv/live_tv_screen.dart';

class SourcesScreen extends StatelessWidget {
  const SourcesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F1014),
      appBar: AppBar(
        title: const Text('Add Provider Source', style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: ListView(
        padding: const EdgeInsets.all(24.0),
        children: [
          _buildSourceCard(context, 'M3U URL / Playlist', 'Add a standard IPTV playlist URL', Icons.link),
          _buildSourceCard(context, 'Xtream Codes', 'Login with Xtream Codes API', Icons.tv),
          _buildSourceCard(context, 'MAC Portal (Stalker)', 'Connect using MAC address', Icons.settings_ethernet),
          _buildSourceCard(context, 'Emby / Jellyfin', 'Connect to your personal media server', Icons.dns),
          _buildSourceCard(context, 'Plex', 'Login with your Plex account', Icons.play_circle_filled),
          const SizedBox(height: 30),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
              backgroundColor: const Color(0xFFE50914),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            ),
            onPressed: () {
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(builder: (context) => const LiveTVScreen()),
              );
            },
            child: const Text('Continue to App', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
          )
        ],
      ),
    );
  }

  Widget _buildSourceCard(BuildContext context, String title, String subtitle, IconData icon) {
    return Card(
      color: const Color(0xFF1E1E24),
      margin: const EdgeInsets.only(bottom: 16),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
        leading: Icon(icon, size: 32, color: Colors.white),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
        subtitle: Text(subtitle, style: const TextStyle(color: Colors.grey)),
        trailing: const Icon(Icons.arrow_forward_ios, size: 16, color: Colors.grey),
        onTap: () {
          // Placeholder for source configuration dialog
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Configure $title...')),
          );
        },
      ),
    );
  }
}
