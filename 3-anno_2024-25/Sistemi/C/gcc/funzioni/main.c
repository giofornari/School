#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include "vectLib.h"  // Assicurarsi che il file header contenga le dichiarazioni delle funzioni

int main() {
    // ------ Test iniziale: fill_vec() e print_vec() ------
    double v1[5];
    fill_vec(v1, 5, 1.0); // Inizializza v1 con tutti 1.0
    printf("v1 (tutti 1.0): ");
    print_vec(v1, 5);

    // ------ Test di add_vec(): somma elemento per elemento ------
    double v2[5];
    fill_vec(v2, 5, 2.0); // v2: tutti 2.0
    double res_add[5];
    add_vec(v1, v2, res_add, 5); // v1 + v2: ogni elemento dovrebbe diventare 3.0
    printf("v1 + v2: ");
    print_vec(res_add, 5);

    // ------ Test di adds_vec(): somma di uno scalare a ogni elemento ------
    double res_adds[5];
    adds_vec(v1, 3.0, res_adds, 5); // v1 + 3: ogni elemento diventa 4.0
    printf("v1 + 3: ");
    print_vec(res_adds, 5);

    // ------ Test di muls_vec(): moltiplicazione per scalare ------
    double res_muls[5];
    muls_vec(v1, 4.0, res_muls, 5); // v1 * 4: ogni elemento diventa 4.0
    printf("v1 * 4: ");
    print_vec(res_muls, 5);

    // ------ Test di sub_vec(): sottrazione elemento per elemento ------
    // (Attenzione: l'implementazione data potrebbe contenere errori, qui ci aspettiamo v1 - v2 = -1 in ogni elemento)
    double res_sub[5];
    sub_vec(v1, v2, res_sub, 5);
    printf("v1 - v2: ");
    print_vec(res_sub, 5);

    // ------ Test di dot_vec(): prodotto scalare ------
    double dot = dot_vec(v1, v2, 5); // 1*2 * 5 elementi = 10
    printf("Prodotto scalare (v1 . v2): %lf\n", dot);

    // ------ Test di concat_vec(): concatenazione di due vettori ------
    double v3[10];
    concat_vec(v1, 5, v2, 5, v3);
    printf("Concatenazione di v1 e v2: ");
    print_vec(v3, 10);

    // ------ Test di reverse_vec(): inversione dell'ordine degli elementi ------
    double v1_copy[5];
    // Creiamo un vettore [1, 2, 3, 4, 5]
    for (int i = 0; i < 5; i++) {
        v1_copy[i] = 1.0 + i;
    }
    printf("v1_copy prima di reverse: ");
    print_vec(v1_copy, 5);
    reverse_vec(v1_copy, 5);
    printf("v1_copy dopo reverse: ");
    print_vec(v1_copy, 5);

    // ------ Test di sort_vec(): ordinamento in ordine crescente ------
    double v_unsorted[5] = {5.0, 3.0, 4.0, 1.0, 2.0};
    printf("v_unsorted prima di sort: ");
    print_vec(v_unsorted, 5);
    sort_vec(v_unsorted, 5);
    printf("v_unsorted dopo sort: ");
    print_vec(v_unsorted, 5);

    // ------ Test di shuffle_vec(): mescola gli elementi in modo casuale ------
    double v_shuffle[5] = {1.0, 2.0, 3.0, 4.0, 5.0};
    printf("v_shuffle prima di shuffle: ");
    print_vec(v_shuffle, 5);
    shuffle_vec(v_shuffle, 5);
    printf("v_shuffle dopo shuffle: ");
    print_vec(v_shuffle, 5);

    // ------ Test di rshft_vec(): shift a destra ------
    double v_rshft[5] = {1, 2, 3, 4, 5};
    printf("v_rshft prima di right shift: ");
    print_vec(v_rshft, 5);
    rshft_vec(v_rshft, 2, 5);  // sposta a destra di 2 posizioni, elementi in uscita diventano 0
    printf("v_rshft dopo right shift di 2: ");
    print_vec(v_rshft, 5);

    // ------ Test di lshft_vec(): shift a sinistra ------
    double v_lshft[5] = {1, 2, 3, 4, 5};
    printf("v_lshft prima di left shift: ");
    print_vec(v_lshft, 5);
    lshft_vec(v_lshft, 2, 5);  // sposta a sinistra di 2 posizioni, elementi in uscita diventano 0
    printf("v_lshft dopo left shift di 2: ");
    print_vec(v_lshft, 5);

    // ------ Test di rrot_vec(): rotazione a destra ------
    double v_rrot[5] = {1, 2, 3, 4, 5};
    printf("v_rrot prima di right rotation: ");
    print_vec(v_rrot, 5);
    rrot_vec(v_rrot, 2, 5);  // ruota a destra di 2 posizioni, gli elementi usciti rientrano in testa
    printf("v_rrot dopo right rotation di 2: ");
    print_vec(v_rrot, 5);

    // ------ Test di lrot_vec(): rotazione a sinistra ------
    double v_lrot[5] = {1, 2, 3, 4, 5};
    printf("v_lrot prima di left rotation: ");
    print_vec(v_lrot, 5);
    lrot_vec(v_lrot, 2, 5);  // ruota a sinistra di 2 posizioni (nota: l'implementazione potrebbe avere errori)
    printf("v_lrot dopo left rotation di 2: ");
    print_vec(v_lrot, 5);

    // ------ Test di slice_vec(): estrazione di una porzione del vettore ------
    double slice[3];
    // Supponiamo di voler estrarre 3 elementi a partire dalla posizione 1 di v1_copy (che ora è invertito)
    slice_vec(v1_copy, slice, 1, 3);
    printf("Slice di v1_copy (dalla posizione 1 per 3 elementi): ");
    print_vec(slice, 3);

    // ------ Test di norm_vec(), mean_vec(), min_vec(), max_vec(), sum_vec() ------
    double norm = norm_vec(v1, 5);
    printf("Norma di v1: %lf\n", norm);

    double mean = mean_vec(v1, 5);
    printf("Media di v1: %lf\n", mean);

    double min_val = min_vec(v1, 5);
    printf("Minimo di v1: %lf\n", min_val);

    double max_val = max_vec(v1, 5);
    printf("Massimo di v1: %lf\n", max_val);

    double sum = sum_vec(v1, 5);
    printf("Somma di v1: %lf\n", sum);

    // ------ Test di eq_vec(): confronto di vettori con tolleranza ------
    bool eq = eq_vec(v1, v1, 5, 0.0001);
    printf("v1 uguale a se stesso (tolleranza 0.0001): %s\n", eq ? "true" : "false");

    // ------ Test di map_vec(): applica una funzione (qui sqrt) a ogni elemento ------
    double v_map[5];
    // Costruiamo un vettore con valori diversi
    for (int i = 0; i < 5; i++) {
        v_map[i] = v2[i] * (i + 1); // otteniamo [2, 4, 6, 8, 10]
    }
    printf("v_map prima di map_vec (sqrt): ");
    print_vec(v_map, 5);
    map_vec(v_map, 5, sqrt);  // applica la radice quadrata a ogni elemento
    printf("v_map dopo map_vec (sqrt): ");
    print_vec(v_map, 5);

    return 0;
}
