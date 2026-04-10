import 'package:flutter/material.dart';
import 'dart:math';

void main() {
  runApp(const SpiridicchioApp());
}

class SpiridicchioApp extends StatelessWidget {
  const SpiridicchioApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Spiridicchio',
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0A0A0A),
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.deepPurpleAccent,
          brightness: Brightness.dark,
          primary: Colors.cyanAccent,
          secondary: Colors.pinkAccent,
        ),
        useMaterial3: true,
      ),
      home: const CentralinaPage(),
    );
  }
}

class CentralinaPage extends StatefulWidget {
  const CentralinaPage({super.key});

  @override
  State<CentralinaPage> createState() => _CentralinaPageState();
}

class _CentralinaPageState extends State<CentralinaPage>
    with SingleTickerProviderStateMixin {
  int _aura = 0;
  final Random _random = Random();
  late AnimationController _glitchController;

  @override
  void initState() {
    super.initState();
    _glitchController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 100),
    );
  }

  @override
  void dispose() {
    _glitchController.dispose();
    super.dispose();
  }

  void _mettiAura() {
    setState(() {
      _aura += (_random.nextInt(100) + 10) * 10;
    });
    _glitchController.forward(from: 0.0);
  }

  void _sputtanaAura() {
    setState(() {
      _aura -= (_random.nextInt(500) + 50) * 10;
    });
    _glitchController.forward(from: 0.0);
  }

  void _showCentralina() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: Colors.black87,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(30),
          side: const BorderSide(color: Colors.redAccent, width: 3),
        ),
        title: const Text(
          "LA CENTRALINA",
          style: TextStyle(
            color: Colors.redAccent,
            fontWeight: FontWeight.bold,
            letterSpacing: 2,
          ),
        ),
        content: const Text(
          "Lascia stare... è un casino.",
          style: TextStyle(color: Colors.white, fontSize: 18),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text(
              "HO CAPITO",
              style: TextStyle(color: Colors.cyanAccent),
            ),
          ),
        ],
      ),
    );
  }

  void _spiridicchioPhrase() {
    ScaffoldMessenger.of(context).clearSnackBars();
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        backgroundColor: Colors.pinkAccent,
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        content: const Row(
          children: [
            Icon(Icons.auto_awesome, color: Colors.white),
            SizedBox(width: 10),
            Expanded(
              child: Text(
                "He bella osa he hai detto bro 🗿",
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Stack(
          children: [
            // Background decorations
            Positioned(
              top: -50,
              left: -50,
              child: Container(
                width: 200,
                height: 200,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: Colors.deepPurpleAccent.withOpacity(0.3),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.deepPurpleAccent.withOpacity(0.5),
                      blurRadius: 100,
                    ),
                  ],
                ),
              ),
            ),
            Positioned(
              bottom: -100,
              right: -50,
              child: Container(
                width: 300,
                height: 300,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: Colors.cyanAccent.withOpacity(0.2),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.cyanAccent.withOpacity(0.4),
                      blurRadius: 120,
                    ),
                  ],
                ),
              ),
            ),

            // Main Content
            Center(
              child: SingleChildScrollView(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 24.0),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text(
                        "S P I R I D I C C H I O",
                        style: TextStyle(
                          fontSize: 32,
                          fontWeight: FontWeight.w900,
                          letterSpacing: 8,
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(height: 60),
                      AnimatedBuilder(
                        animation: _glitchController,
                        builder: (context, child) {
                          return Transform.translate(
                            offset: Offset(
                              _random.nextDouble() *
                                  10 *
                                  _glitchController.value,
                              _random.nextDouble() *
                                  10 *
                                  _glitchController.value,
                            ),
                            child: Container(
                              padding: const EdgeInsets.all(30),
                              decoration: BoxDecoration(
                                color: Colors.black54,
                                borderRadius: BorderRadius.circular(40),
                                border: Border.all(
                                  color: _aura >= 0
                                      ? Colors.cyanAccent
                                      : Colors.redAccent,
                                  width: 4,
                                ),
                                boxShadow: [
                                  BoxShadow(
                                    color: _aura >= 0
                                        ? Colors.cyanAccent.withOpacity(0.5)
                                        : Colors.redAccent.withOpacity(0.5),
                                    blurRadius:
                                        30 + (20 * _glitchController.value),
                                    spreadRadius: 5,
                                  ),
                                ],
                              ),
                              child: Column(
                                children: [
                                  const Text(
                                    "AURA ATTUALE",
                                    style: TextStyle(
                                      color: Colors.white70,
                                      letterSpacing: 3,
                                    ),
                                  ),
                                  const SizedBox(height: 10),
                                  Text(
                                    "$_aura",
                                    style: TextStyle(
                                      fontSize: 80,
                                      height: 1,
                                      fontWeight: FontWeight.w900,
                                      color: _aura >= 0
                                          ? Colors.white
                                          : Colors.red,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          );
                        },
                      ),
                      const SizedBox(height: 70),

                      // Action Buttons
                      Row(
                        children: [
                          Expanded(
                            child: ElevatedButton(
                              onPressed: _sputtanaAura,
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.redAccent,
                                foregroundColor: Colors.white,
                                padding: const EdgeInsets.symmetric(
                                  vertical: 20,
                                ),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(20),
                                ),
                                elevation: 10,
                              ),
                              child: const Text(
                                "SPUTTANA\nSTRA AURA",
                                textAlign: TextAlign.center,
                                style: TextStyle(
                                  fontWeight: FontWeight.w900,
                                  fontSize: 16,
                                ),
                              ),
                            ),
                          ),
                          const SizedBox(width: 20),
                          Expanded(
                            child: ElevatedButton(
                              onPressed: _mettiAura,
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.cyanAccent,
                                foregroundColor: Colors.black,
                                padding: const EdgeInsets.symmetric(
                                  vertical: 20,
                                ),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(20),
                                ),
                                elevation: 10,
                              ),
                              child: const Text(
                                "METTI\nAURA",
                                textAlign: TextAlign.center,
                                style: TextStyle(
                                  fontWeight: FontWeight.w900,
                                  fontSize: 16,
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 30),

                      // Extra chaotic options
                      SizedBox(
                        width: double.infinity,
                        child: OutlinedButton(
                          onPressed: _showCentralina,
                          style: OutlinedButton.styleFrom(
                            side: const BorderSide(
                              color: Colors.amberAccent,
                              width: 2,
                            ),
                            padding: const EdgeInsets.symmetric(vertical: 20),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(20),
                            ),
                          ),
                          child: const Text(
                            "CENTRALINA",
                            style: TextStyle(
                              color: Colors.amberAccent,
                              fontWeight: FontWeight.bold,
                              letterSpacing: 2,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 15),
                      SizedBox(
                        width: double.infinity,
                        child: OutlinedButton(
                          onPressed: _spiridicchioPhrase,
                          style: OutlinedButton.styleFrom(
                            side: const BorderSide(
                              color: Colors.pinkAccent,
                              width: 2,
                            ),
                            padding: const EdgeInsets.symmetric(vertical: 20),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(20),
                            ),
                          ),
                          child: const Text(
                            "SPIRIDICCHIO VIBES",
                            style: TextStyle(
                              color: Colors.pinkAccent,
                              fontWeight: FontWeight.bold,
                              letterSpacing: 2,
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
