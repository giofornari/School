#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <limits>



using std::string;
using namespace std;

char welcome_msg[5][400] = {
    "\n\n############################################################################################################################\n\n",
    "\t\t\t   Benvenuto nel migliore programma di gestione dei fagiani! \n", 
    "\t\t\t  Inserisci i dati dei fagiani e calcoleremo il guadagno totale!",
    "\n\n############################################################################################################################\n\n",
};


char instructions[4][400] = {
    "|                                                                        |\n",
    "| Ora inserirai alcuni dati dei fagiani di cui vuoi ricavare il guadagno |\n",
    "|                                                                        |\n",

};
int num_fagiani;
struct Fagiano {
    char nome[50];
    int uova;
    float peso;
};
 
int main() {
    
    for (int i = 0; i < 4; i++) {
        cout << welcome_msg[i] << endl;
    }
    for (int i=0; i<3; i++) {
        cout << instructions[i] << endl;
    }
    cout << "Quanti fagiani vuoi inserire? (max 1000): ";
    while (true) {
        cin >> num_fagiani;
        if (cin.fail() || num_fagiani <= 0 || num_fagiani > 1000) {
            cin.clear();
            cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            cerr << "Errore: inserisci un numero intero valido tra 1 e 1000." << endl;
        } else {
            break;
        }
    }
    Fagiano fagiano[num_fagiani];
    for (int i = 0; i < num_fagiani; i++) {
        cout << "Inserisci il nome del fagiano " << i+1 << ":" << endl;
        cin >> fagiano[i].nome;
        cout << "Inserisci il numero di uova del fagiano: " << i << endl;
        while (true) {
            cin >> fagiano[i].uova;
            if (cin.fail()) {
                cin.ignore(std::numeric_limits<int>::max()); // discard invalid input
                cerr << "Errore: inserisci un numero intero valido per le uova." << endl;
                fflush(stdin);
            } else if (fagiano[i].uova < 0) {
                cerr << "Errore: inserisci un numero intero positivo per le uova." << endl;
                fflush(stdin);
            } else {
                break;
            }
        }

        cout << "Inserisci il peso (kg) del fagiano: " << i << endl;
        while (true) {
            cin >> fagiano[i].peso;
            if (cin.fail()) {
                cin.clear();
                cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
                cerr << "Errore: inserisci un numero intero valido di peso." << endl;
                fflush(stdin);
            } else if (fagiano[i].peso < 0) {
                cerr << "Errore: inserisci un numero intero positivo per le uova." << endl;
                fflush(stdin);
            } else {
                break;
            }
        }
    }

    FILE *output = fopen("fagiani.dat", "wb");

    if (output == NULL) {
        cerr << "Errore nell'apertura del file." << endl;
        return 1;
    }

    for (int i = 0; i < num_fagiani; i++) {
        fwrite(&fagiano[i], sizeof(Fagiano), 1, output);
    }


    fclose(output);
    char file_message[4][200] = {
        "\n\n############################################################################################################################\n\n",
        "\t\t\t   I dati sono stati salvati correttamente nel file fagiani.dat! \n",
        "\t\t\t  Ora calcoleremo il guadagno totale!",
        "\n\n############################################################################################################################\n\n",
    };
    for (int i = 0; i < 4; i++) {
        cout << file_message[i] << endl;
    }

    Fagiano fagiano_letto[num_fagiani];
    FILE *input = fopen("fagiani.dat", "rb");

    if (input == NULL) {
        cerr << "Errore nell'apertura del file." << endl;
        return 1;
    }

    for (int i = 0; i < num_fagiani; i++) {
        fread(&fagiano_letto[i], sizeof(Fagiano), 1, input);
    }

    fclose(input);

    int tot_uova = 0;

    for (int i = 0; i < num_fagiani; i++) {
        tot_uova += fagiano_letto[i].uova;
    }
    float tot_weight = tot_uova * 0.01;

    for (int i = 0; i < num_fagiani; i++) {
        tot_weight += fagiano_letto[i].peso;
    }

    cout << "Il totale delle uova è: " << tot_uova << endl;
    cout << "Il totale del peso dei fagiani e delle loro uova è: " << tot_weight << " kg" << endl;
    float income = tot_weight * 25.7;
    cout << "Il guadagno è: " << income << " \u20AC" << endl; // code for euro symbol

    cout << "Vorresti vendere " << num_fagiani << " amici.\n" << endl;
    for (int i = 0; i< num_fagiani; i++) {
        cout << fagiano[i].nome << "\n" << endl;
        }
    cout << "Questi sono i nomi degli amici che perderai. Pensaci bene.\n\n\n" << endl;
    return 0;
    
}