import 'package:flutter/material.dart';

/// Semplice Widget che riscrive su un Text in valore di un TextField con evento
/// onPressed su Bottone.
/// Introduce l'uso di TextEditingController() che produce un oggetto relativo
/// da assegnare alla proprietà controller dei Widget TextField a cui ci si può
/// accedere al di fuori del widget stesso per ottenerne il testo editato,
/// es. nell'ascoltatore di un Button.

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Convertitore euro-dollari',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.red.shade900,
          brightness: Brightness.light,
        ),
        inputDecorationTheme: InputDecorationTheme(
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          filled: true,
          fillColor: Colors.red.withAlpha(25),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
      ),
      darkTheme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.red.shade900,
          brightness: Brightness.dark,
        ),
        inputDecorationTheme: InputDecorationTheme(
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          filled: true,
          fillColor: Colors.white.withAlpha(25),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
      ),
      home: const HomePageProva(title: 'Convertitore euro-dollari'),
    );
  }
}

class HomePageProva extends StatefulWidget {
  const HomePageProva({super.key, required this.title});

  final String title;

  @override
  _HomePageProvaState createState() => _HomePageProvaState();
}

class _HomePageProvaState extends State<HomePageProva> {
  String _msg = "";
  // servirà per accedere dinamicamente (runtime) al widget TextField
  final _controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.title)),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Text(
                'Inserisci la cifra in euro:',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _controller,
                keyboardType: const TextInputType.numberWithOptions(
                  decimal: true,
                ),
                textAlign: TextAlign.center,
                decoration: const InputDecoration(
                  hintText: '0.00',
                  suffixText: '€',
                ),
              ),
              const SizedBox(height: 24),
              ElevatedButton.icon(
                icon: const Icon(Icons.currency_exchange),
                label: const Text('Converti'),
                onPressed: () {
                  setState(() {
                    final text = _controller.text;
                    if (text.isEmpty) {
                      _msg = "0.00";
                      return;
                    }
                    final euro = double.tryParse(text.replaceAll(',', '.'));
                    if (euro != null) {
                      _msg = (euro * 1.09).toStringAsFixed(2);
                    } else {
                      _msg = "Errore";
                    }
                  });
                },
              ),
              Padding(
                padding: const EdgeInsets.only(top: 20),
                child: Text(
                  'La cifra corrisponde a: $_msg \$',
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
