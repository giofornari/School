// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter_test/flutter_test.dart';

import 'package:spiridicchio/main.dart';

void main() {
  testWidgets('Aura updates test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const SpiridicchioApp());

    // Verify that our aura starts at 0.
    expect(find.text('0'), findsOneWidget);

    // Tap the 'METTI AURA' button and trigger a frame.
    await tester.tap(find.textContaining('METTI'));
    await tester.pump();

    // Verify that our aura has changed based on randomness (not 0 anymore in real terms, but smoke test passing)
    expect(find.text('0'), findsNothing);
  });
}
