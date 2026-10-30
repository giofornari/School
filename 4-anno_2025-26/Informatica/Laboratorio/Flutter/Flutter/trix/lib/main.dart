import 'dart:math';

import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Tris',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: const TrisPage(),
    );
  }
}

class TrisPage extends StatefulWidget {
  const TrisPage({super.key});
  @override
  State<TrisPage> createState() => _TrisPageState();
}

class _TrisPageState extends State<TrisPage> {
  List<String> cells = List.generate(9, (_) => '');
  String player = Random().nextBool() ? 'X' : 'O';
  String winner = '';

  // tutte le combinazioni vincenti
  static const wins = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6],
  ];

  String checkWinner() {
    for (var w in wins) {
      String a = cells[w[0]], b = cells[w[1]], c = cells[w[2]];
      if (a != '' && a == b && b == c) return a;
    }
    if (cells.every((c) => c != '')) return 'pareggio';
    return '';
  }

  void click(int i) {
    if (cells[i] != '' || winner != '') return;
    setState(() {
      cells[i] = player;
      winner = checkWinner();
      if (winner == '') player = player == 'X' ? 'O' : 'X';
    });
  }

  void reset() {
    setState(() {
      cells = List.generate(9, (_) => '');
      player = Random().nextBool() ? 'X' : 'O';
      winner = '';
    });
  }

  Widget cellIcon(String val) {
    if (val == 'X') {
      return const Icon(Icons.close, size: 52, color: Colors.red);
    }
    if (val == 'O') {
      return const Icon(Icons.radio_button_unchecked, size: 52, color: Colors.blue);
    }
    return const SizedBox();
  }

  @override
  Widget build(BuildContext context) {
    String status = winner == ''
        ? 'turno: $player'
        : winner == 'pareggio'
            ? 'pareggio!'
            : 'vince: $winner!';

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Tris'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(status, style: const TextStyle(fontSize: 24)),
            const SizedBox(height: 20),
            SizedBox(
              width: 310,
              height: 310,
              child: GridView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 3,
                  mainAxisSpacing: 8,
                  crossAxisSpacing: 8,
                ),
                itemCount: 9,
                itemBuilder: (context, i) {
                  return ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.orangeAccent,
                      elevation: 12,
                    ),
                    onPressed: () => click(i),
                    child: cellIcon(cells[i]),
                  );
                },
              ),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: reset,
              child: const Text('ricomincia'),
            ),
          ],
        ),
      ),
    );
  }
}
