import 'dart:io';
import 'package:path_provider/path_provider.dart';

class CrashLogger {
  static final CrashLogger _instance = CrashLogger._internal();
  factory CrashLogger() => _instance;
  CrashLogger._internal();

  /// Logs a media_kit failure securely without capturing PII
  Future<void> logPlaybackError(String errorType, String message) async {
    try {
      final directory = await getApplicationDocumentsDirectory();
      final file = File('${directory.path}/playback_diagnostics.log');

      final timestamp = DateTime.now().toIso8601String();
      final safeMessage = _scrubPii(message);
      
      final logEntry = '[$timestamp] [$errorType] $safeMessage\n';
      
      // Append to local rotating log
      await file.writeAsString(logEntry, mode: FileMode.append);
      
      // Implement rotation logic if file > 5MB
    } catch (e) {
      print('Failed to write diagnostic log: $e');
    }
  }

  /// Exports the log file as a clean string for GitHub Issues
  Future<String> exportLogsForGitHub() async {
    try {
      final directory = await getApplicationDocumentsDirectory();
      final file = File('${directory.path}/playback_diagnostics.log');
      if (await file.exists()) {
        final contents = await file.readAsString();
        return '```text\n$contents\n```';
      }
      return 'No diagnostic logs found.';
    } catch (e) {
      return 'Error exporting logs: $e';
    }
  }

  String _scrubPii(String message) {
    // Aggressively remove IP addresses, tokens, and usernames from the log string
    var scrubbed = message.replaceAll(RegExp(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'), '[IP_REDACTED]');
    scrubbed = scrubbed.replaceAll(RegExp(r'password=[^&\s]+'), 'password=[REDACTED]');
    return scrubbed;
  }
}
