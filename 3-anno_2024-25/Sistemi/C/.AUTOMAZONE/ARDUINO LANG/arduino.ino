/*
@bigBrodyG - 2025

Questo programma è un semplice calcolatore che utilizza un display LCD e una tastiera a matrice 4x4.

Il programma permette di inserire numeri e operazioni aritmetiche (+, -, *, /) tramite la tastiera.
Il risultato viene visualizzato sul display LCD.


##pin digitali dell'Arduino ai quali il display LCD è collegato:

12  --> Pin RS (Register Select)
11  --> Pin E (Enable)
5   --> Pin D4 (Data line 4)
4   --> Pin D5 (Data line 5)
3   --> Pin D6 (Data line 6)
2   --> Pin D7 (Data line 7)

##pin analogici dell'Arduino ai quali la tastiera è collegata:

10, 9, 8, 7 --> Pin righe
A3, A2, A1, A0 --> Pin colonne

*/

#include <LiquidCrystal.h>
#include <Keypad.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);


void setup() {
  lcd.begin(16, 2);
  lcd.print("Calcolatrice!!");
  lcd.setCursor(0,1);
}

const byte RIGHE = 4; 
const byte COLONNE = 4; 
char keys[RIGHE][COLONNE] = {
    {'1','2','3','+'},
    {'4','5','6','-'},
    {'7','8','9','*'},
    {'C','0','=','/'}
};
byte rpin[RIGHE] = {10, 9, 8, 7}; 
byte cpin[COLONNE] = {A3, A2, A1, A0}; 

Keypad keypad = Keypad(makeKeymap(keys), rpin, cpin, RIGHE, COLONNE);

String scalcolo = "";
char operatore;
float risultato = 0;

void loop() {
    char key = keypad.getKey();

    if (key) {
        if (key >= '0' && key <= '9') {
            scalcolo += key;
            lcd.print(scalcolo);
        } else if (key == 'C') {
            scalcolo = "";
            risultato = 0;
            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print("Cleared");
            delay(1000);
            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print("Calcolatrice!!");
            lcd.setCursor(0, 1);
        } else if (key == '=') {
            float currentNumber = scalcolo.toFloat();
            if (operatore == '+') risultato += currentNumber;
            else if (operatore == '-') risultato -= currentNumber;
            else if (operatore == '*') risultato *= currentNumber;
            else if (operatore == '/') risultato /= currentNumber;

            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print("risultato:");
            lcd.setCursor(0, 1);
            lcd.print(risultato);
            scalcolo = "";
        } else {
            if (scalcolo.length() > 0) {
                float currentNumber = scalcolo.toFloat();
                if (operatore == 0) risultato = currentNumber;
                else if (operatore == '+') risultato += currentNumber;
                else if (operatore == '-') risultato -= currentNumber;
                else if (operatore == '*') risultato *= currentNumber;
                else if (operatore == '/') risultato /= currentNumber;

                operatore = key;
                scalcolo = "";
                lcd.print(operatore);
            }
        }
    }
}

