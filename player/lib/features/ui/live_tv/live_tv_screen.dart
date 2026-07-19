import 'package:flutter/material.dart';

class LiveTVScreen extends StatelessWidget {
  const LiveTVScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Live TV (OTT Navigator UI)'),
      ),
      body: Row(
        children: [
          // Sidebar for Categories/Countries
          Expanded(
            flex: 2,
            child: Container(
              color: Colors.grey[900],
              child: ListView(
                children: const [
                  ListTile(title: Text('All Channels')),
                  ListTile(title: Text('Sports')),
                  ListTile(title: Text('News')),
                  // Add dynamically parsed categories here
                ],
              ),
            ),
          ),
          // Center for Channels
          Expanded(
            flex: 3,
            child: Container(
              color: Colors.grey[850],
              child: ListView(
                children: const [
                  ListTile(title: Text('Channel 1')),
                  ListTile(title: Text('Channel 2')),
                ],
              ),
            ),
          ),
          // Right panel for EPG and Mini Player
          Expanded(
            flex: 4,
            child: Container(
              color: Colors.black,
              child: Column(
                children: [
                  // Mini Player Placeholder
                  Container(
                    height: 250,
                    color: Colors.black87,
                    child: const Center(
                      child: Text('MediaKit Video Player Here'),
                    ),
                  ),
                  // EPG Info
                  Expanded(
                    child: Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: const Text('EPG Data: Currently playing...'),
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
}
