import 'package:flutter/material.dart';

void main() {
  runApp(const AuraBuilder());
}

class AuraBuilder extends StatelessWidget {
  const AuraBuilder({super.key});

  static const List<String> _immagini = <String>[
    'lib/aura/aura7.png',
    'lib/aura/aura8.png',
    'lib/aura/aura9.png',
    'lib/aura/aura10.png',
    'lib/aura/aura11.png',
    'lib/aura/aura12.png',
  ];

  @override
  Widget build(BuildContext context) {
    const title = 'AURA GRID - BUILDER';

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
          child: GridView.builder(
            itemCount: _immagini.length,
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 2,
              crossAxisSpacing: 12,
              mainAxisSpacing: 12,
            ),
            itemBuilder: (BuildContext context, int index) {
              return AuraTile(imagePath: _immagini[index]);
            },
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
    return Material(
      color: Colors.transparent,
      child: ClipRRect(
        borderRadius: BorderRadius.circular(16),
        child: Image.asset(imagePath, fit: BoxFit.cover),
      ),
    );
  }
}
