#include <stdlib.h>
#include <iostream>
#include <string>
#include <fstream>
#include <limits>

using std::string;
using namespace std;
int num_fagiani;

struct Fagiano {
    char nome[50];
    int uova;
    float peso;
};

int main() {

    cout << "Quanti fagiani vuoi inserire? (max 1000): ";
    cin >> num_fagiani;
    Fagiano fagiano[num_fagiani];

    for (int i = 0; i < num_fagiani; i++) {
        cout << "Inserisci il nome del fagiano " << i+1 << ":" << endl;
        cin >> fagiano[i].nome;
        cout << "Inserisci il numero di uova del fagiano: " << i << endl;
        cin >> fagiano[i].uova;
        cout << "Inserisci il peso (kg) del fagiano: " << i << endl;
        cin >> fagiano[i].peso;
    }

    FILE *output = fopen("fagiani.dat", "wb");



    for (int i = 0; i < num_fagiani; i++) {
        fwrite(&fagiano[i], sizeof(Fagiano), 1, output);
    }


    fclose(output);
    
    Fagiano fagiano_letto[num_fagiani];
    FILE *input = fopen("fagiani.dat", "rb");

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
    cout << "Il totale del peso è: " << tot_weight << " kg" << endl;
    float income = tot_weight * 25.7;
    cout << "Il guadagno è: " << income << " euro" << endl;
    return 0;
    
}