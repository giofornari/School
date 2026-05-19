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
      title: 'Impiccato',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
      ),
      home: const ImpiccatoPage(),
    );
  }
}

class ImpiccatoPage extends StatefulWidget {
  const ImpiccatoPage({super.key});
  @override
  State<ImpiccatoPage> createState() => _ImpiccatoPageState();
}

class _ImpiccatoPageState extends State<ImpiccatoPage> {
  // parole da indovinare
  static const parole = [
    'computer', 'tastiera', 'schermo', 'flutter', 'android',
    'programma', 'variabile', 'funzione', 'algoritmo', 'database',
  ];

  late String parola;
  List<String> indovinate = [];
  List<String> sbagliate = [];
  final ctrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    newGame();
  }

  @override
  void dispose() {
    ctrl.dispose();
    super.dispose();
  }

  void newGame() {
    parola = parole[Random().nextInt(parole.length)];
    indovinate = [];
    sbagliate = [];
    ctrl.clear();
  }

  // 10 errori max (immagini 0..10)
  int get errori => sbagliate.length;
  bool get perso => errori >= 10;
  bool get vinto => parola.split('').every((c) => indovinate.contains(c));

  void guess() {
    String lettera = ctrl.text.toLowerCase().trim();
    ctrl.clear();
    if (lettera.isEmpty || lettera.length != 1) return;
    if (!RegExp(r'[a-z]').hasMatch(lettera)) return;
    if (indovinate.contains(lettera) || sbagliate.contains(lettera)) return;
    if (vinto || perso) return;
    setState(() {
      if (parola.contains(lettera)) {
        indovinate.add(lettera);
      } else {
        sbagliate.add(lettera);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    // mostra _ per lettere non ancora indovinate
    String display = parola.split('').map((c) => indovinate.contains(c) ? c : '_').join(' ');

    String status = vinto
        ? 'hai vinto!'
        : perso
            ? 'hai perso! era: $parola'
            : '';

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('impiccato'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // immagine impiccato corrente
            Image.asset('assets/$errori.png', width: 220, height: 220),
            const SizedBox(height: 12),
            Text(
              display,
              style: const TextStyle(fontSize: 28, letterSpacing: 6),
            ),
            const SizedBox(height: 8),
            if (sbagliate.isNotEmpty)
              Text(
                'sbagliate: ${sbagliate.join(', ')}',
                style: const TextStyle(fontSize: 16, color: Colors.red),
              ),
            const SizedBox(height: 16),
            // input lettera con TextField e controller
            if (!vinto && !perso) ...[
              SizedBox(
                width: 200,
                child: TextField(
                  controller: ctrl,
                  maxLength: 1,
                  textInputAction: TextInputAction.done,
                  decoration: const InputDecoration(
                    labelText: 'inserisci una lettera',
                    counterText: '',
                  ),
                  onSubmitted: (_) => guess(),
                ),
              ),
              const SizedBox(height: 8),
              ElevatedButton(
                onPressed: guess,
                child: const Text('prova'),
              ),
            ],
            if (status.isNotEmpty) ...[
              const SizedBox(height: 16),
              Text(status, style: const TextStyle(fontSize: 22)),
              const SizedBox(height: 8),
              ElevatedButton(
                onPressed: () => setState(newGame),
                child: const Text('nuovo gioco'),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
