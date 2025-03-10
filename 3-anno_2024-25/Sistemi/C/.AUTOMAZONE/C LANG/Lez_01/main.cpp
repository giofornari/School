#include <iostream>
using namespace std;
/*
STD : : è detto "scope resolution operator" e serve per specificare a quale entità ci si sta riferendo. 
Con std:: ci si riferisce al namespace std. 
Per evitare di doverlo scrivere esplicitamente puoi inserire questo statement prima del main:
using namespace std;

http://www.bo.cnr.it/corsi-di-informatica/corsoCstandard/Lezioni/34Standard.html
*/
int num1 = 15;
int num2 = 0;
int main() {
    cout << "Inserisci un numero intero: ";
    cin >> num2;
    int sum = num1 + num2;
    cout << "La somma del tuo numero e 1 è: " << sum << "\n";
    return 0;
}