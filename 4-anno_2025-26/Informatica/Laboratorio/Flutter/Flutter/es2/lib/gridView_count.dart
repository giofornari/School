import 'package:flutter/material.dart';

void main() {
  runApp(const AuraGrid());
}

class AuraGrid extends StatelessWidget {
  const AuraGrid();

  static const List<String> _frames = <String>[
    'lib/aura/aura1.png',
    'lib/aura/aura2.png',
    'lib/aura/aura3.png',
    'lib/aura/aura4.png',
    'lib/aura/aura5.png',
    'lib/aura/aura6.png',
  ];

  @override
  Widget build(BuildContext context) {
    const title = 'AURA GRID';

    return MaterialApp(
      title: title,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF6A7CF5)),
      ),
      home: Scaffold(
        appBar: AppBar(title: const Text(title), centerTitle: true),
        body: Padding(
          padding: const EdgeInsets.all(20),
          child: GridView.count(
            crossAxisCount: 2,
            crossAxisSpacing: 12,
            mainAxisSpacing: 12,
            children: <Widget>[
              for (final frame in _frames) AuraTile(imagePath: frame),
            ],
          ),
        ),
      ),
    );
  }
}

class AuraTile extends StatelessWidget {
  final String imagePath;

  const AuraTile({super.key, required this.imagePath});

  @override
  Widget build(BuildContext context) {
    return Card(
      clipBehavior: Clip.antiAlias,
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Image.asset(imagePath, fit: BoxFit.cover),
    );
  }
}
