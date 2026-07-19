import 'package:flutter/material.dart';

class VODScreen extends StatelessWidget {
  const VODScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 400.0,
            flexibleSpace: FlexibleSpaceBar(
              title: const Text('Featured Movie'),
              background: Image.network(
                'https://via.placeholder.com/800x400', // TMDB Poster
                fit: BoxFit.cover,
              ),
            ),
          ),
          SliverList(
            delegate: SliverChildListDelegate([
              _buildCategoryCarousel('Trending Now'),
              _buildCategoryCarousel('Action'),
              _buildCategoryCarousel('Comedy'),
            ]),
          ),
        ],
      ),
    );
  }

  Widget _buildCategoryCarousel(String title) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 10),
          SizedBox(
            height: 150,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              itemCount: 10,
              itemBuilder: (context, index) {
                return Container(
                  width: 100,
                  margin: const EdgeInsets.only(right: 10),
                  color: Colors.grey[800],
                  child: const Center(child: Icon(Icons.movie)),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
