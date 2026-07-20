import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'features/ui/live_tv/live_tv_screen.dart';
import 'features/ui/sources_screen.dart';

import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  MediaKit.ensureInitialized();
  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ALL-IN-One-IPTV',
      theme: ThemeData(
        brightness: Brightness.dark,
        primarySwatch: Colors.blue,
      ),
      home: const SourcesScreen(),
    );
  }
}
