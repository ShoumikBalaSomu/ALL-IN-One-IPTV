class SemanticSearchEngine {
  final Map<String, List<String>> _synonymDictionary = {
    'news': ['noticias', 'nouvelles', 'nachrichten', 'bbc', 'cnn', 'al jazeera'],
    'sports': ['deportes', 'football', 'soccer', 'cricket', 'espn', 'sky sports'],
    'movies': ['cinema', 'peliculas', 'hbo', 'cinemax', 'film'],
    'kids': ['infantil', 'cartoons', 'disney', 'nickelodeon']
  };

  /// Tokenizes the search query and applies basic TF-IDF / Synonym Expansion
  List<String> parseQueryIntents(String rawQuery) {
    final lowerQuery = rawQuery.toLowerCase().trim();
    final tokens = lowerQuery.split(RegExp(r'\s+'));
    final expandedTokens = <String>{};

    for (var token in tokens) {
      expandedTokens.add(token);
      
      // Expand synonyms based on local dictionary
      _synonymDictionary.forEach((category, keywords) {
        if (category == token || keywords.contains(token)) {
          expandedTokens.add(category);
          expandedTokens.addAll(keywords);
        }
      });
    }
    
    return expandedTokens.toList();
  }

  /// Calculates a relevance score for a given EPG Title or Channel Name
  double scoreMatch(String targetName, List<String> searchIntents) {
    double score = 0.0;
    final lowerTarget = targetName.toLowerCase();
    
    for (var intent in searchIntents) {
      if (lowerTarget.contains(intent)) {
        // Direct substring match gives a high weight
        score += 1.0; 
      }
      // Note: Full Levenshtein can be added here for typo-tolerance
    }
    return score;
  }

  /// Takes a raw natural voice query (e.g. "Find Spanish News") and returns top M3U matches
  List<dynamic> executeSemanticSearch(String voiceQuery, List<dynamic> allChannels) {
    final intents = parseQueryIntents(voiceQuery);
    
    final scoredChannels = allChannels.map((channel) {
      final score = scoreMatch(channel['name'], intents);
      return {'channel': channel, 'score': score};
    }).where((item) => (item['score'] as double) > 0.0).toList();

    // Sort by highest relevance score
    scoredChannels.sort((a, b) => (b['score'] as double).compareTo(a['score'] as double));
    
    return scoredChannels.map((item) => item['channel']).toList();
  }
}
