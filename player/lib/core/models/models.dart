import 'package:isar/isar.dart';

part 'models.g.dart'; // Isar generated file

@collection
class Channel {
  Id id = Isar.autoIncrement; // Isar auto increment ID
  
  // Playlist metadata
  late String tvgId;
  late String name;
  late String logoUrl;
  late String group; // Country or Category
  
  // Support for Folded Streams (Phase 1)
  // Instead of a single URL, we store a list of URLs. 
  // The player will iterate through them if the primary fails.
  late List<String> fallbackUrls; 

  // Fast access to the current optimal URL index
  int currentUrlIndex = 0; 
  
  String get activeUrl => fallbackUrls[currentUrlIndex];
}

@collection
class VOD {
  Id id = Isar.autoIncrement;
  late String title;
  late String streamUrl;
  late String posterUrl;
  late String description;
  late double rating;
  late String type; // Movie or Series
}

@collection
class EPGProgram {
  Id id = Isar.autoIncrement;
  @Index()
  late String tvgId;
  late String title;
  late String description;
  late DateTime startTime;
  late DateTime endTime;
}
