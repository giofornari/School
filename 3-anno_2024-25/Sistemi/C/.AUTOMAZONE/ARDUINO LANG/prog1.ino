#include <Keypad.h>
const byte ROWS = 4; //four rows
const byte COLS = 4; //four columns

char keys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte colPins[ROWS] = {A0, A1, A2, A3}; //connect to the row pinouts of the keypad
byte rowPins[COLS] = {9, 11, 12, 13}; //connect to the column pinouts of the keypad

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

// Definizione dei pin del display a 7 segmenti


const int segmentA = 2;
const int segmentB = 3;
const int segmentC = 4;
const int segmentD = 5;
const int segmentE = 6;
const int segmentF = 7;
const int segmentG = 8;
const int button = 2;

const int segmentPins[7] = {segmentA, segmentB, segmentC, segmentD, segmentE, segmentF, segmentG};
const bool digitSegments[10][7] = {
  {true, true, true, true, true, true, false}, // 0
  {false, true, true, false, false, false, false}, // 1
  {true, true, false, true, true, false, true}, // 2
  {true, true, true, true, false, false, true}, // 3
  {false, true, true, false, false, true, true}, // 4
  {true, false, true, true, false, true, true}, // 5
  {true, false, true, true, true, true, true}, // 6
  {true, true, true, false, false, false, false}, // 7
  {true, true, true, true, true, true, true}, // 8
  {true, true, true, true, false, true, true} // 9
};

void setup() {
  pinMode(segmentA, OUTPUT);
  pinMode(segmentB, OUTPUT);
  pinMode(segmentC, OUTPUT);
  pinMode(segmentD, OUTPUT);
  pinMode(segmentE, OUTPUT);
  pinMode(segmentF, OUTPUT);
  pinMode(segmentG, OUTPUT);
  pinMode(button, INPUT);
}

void clearDisplay()
{
  digitalWrite(segmentA, LOW);
  digitalWrite(segmentB, LOW);
  digitalWrite(segmentC, LOW);
  digitalWrite(segmentD, LOW);
  digitalWrite(segmentE, LOW);
  digitalWrite(segmentF, LOW);
  digitalWrite(segmentG, LOW);
}

// Funzione per visualizzare un numero sul display a 7 segmenti


void displayNumber(int num) {
  clearDisplay();
  for (int i = 0; i < 7; i++) {
    digitalWrite(segmentPins[i], digitSegments[num][i]);
  }
}
int cont=0;
void loop() {
  char key = keypad.getKey();
  if (key) {
    if (key == 'A') {
      cont = 0;
    } else if (key == 'B') {
      cont--;
    } else if (key == 'C') {
      cont++;
    } else if (key == 'D') {
      cont = 0;
    } else {
      cont = key - '0';
    }
    displayNumber(cont);
  }
  if (digitalRead(button) == HIGH) {
    displayNumber(cont);
    delay(500);
    if (cont > 9) {
      cont = 0;
    } else {
      cont++;
    }
  }
}

