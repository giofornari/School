#include <stdio.h>
#include <stdlib.h>
#include "vectLib.h"
#include <stdbool.h>
#include <math.h>
// —— Input/Output ——

/** Stampa il vettore v ben formattato [v1, v2, ..., vn] */
void print_vec(const double *v, size_t dim) {
    printf("[");
    for (size_t i = 0; i < dim; i++) {
        printf("%.1lf ", v[i]);
    }
    printf("]\n");
}

/** Legge dim valori da stdin e li salva nel vettore v */
void scanf_vec(double *v, size_t dim){
    for (size_t i = 0; i < dim; i++) {
        scanf("%lf", &v[i]);
    }
}
// —— Operazioni algebriche ——
/** res = v1 + v2 elemento per elemento*/
void add_vec(const double *v1, const double *v2, double *res, size_t dim){
    for (size_t i = 0; i < dim; i++) {
        res[i] = v1[i] + v2[i];
    }

}
/** res = v1 + k  per ogni elemento*/
void adds_vec(const double *v1, double k, double *res, size_t dim){
    for (size_t i = 0; i < dim; i++) {
        res[i] = v1[i] + k;
    }
}
/** res = v * k (moltiplicazione per scalare) */
void muls_vec(const double *v, double k, double *res, size_t dim){
    for (size_t i = 0; i < dim; i++) {
        res[i] = v[i] * k;
    }
}
/** res = v1 - v2 ...sfruttare muls_vec() */
void sub_vec(const double *v1, const double *v2, double *res, size_t dim){
    double tmp[dim] = {};
    muls_vec(v2, -1, tmp, dim);
    for (size_t i = 0; i < dim; i++) {
        res[i] = v1[i] + v2[i];
    }
}

/** Prodotto scalare (v1 • v2) */
double dot_vec(const double *v1, const double *v2, size_t dim){
    double res = 0;
    for (size_t i = 0; i < dim; i++) {
        res += v1[i] * v2[i];
    }
    return res;
}

// —— Manipolazione vettori ——
/** Concatena v1 (dim1) e v2 (dim2) in res (dim1 + dim2 elementi) */
void concat_vec(const double *v1, size_t dim1, const double *v2, size_t dim2, double *res){
    for (size_t i = 0; i < dim1; i++) {
        res[i] = v1[i];
    }
    for (size_t i = 0; i < dim2; i++) {
        res[dim1 + i] = v2[i];
    }
}
/** Inverte l'ordine degli elementi (es. [1,2,3] → [3,2,1]) */
void reverse_vec(double *v, size_t dim){
    for (size_t i = 0; i < dim / 2; i++) {
        double tmp = v[i];
        v[i] = v[dim - i - 1];
        v[dim - i - 1] = tmp;
    }
}
/** Ordina gli elementi in ordine crescente */
void sort_vec(double *v, size_t dim) {
    for (size_t i = 0; i < dim - 1; i++) {
        for (size_t j = i + 1; j < dim; j++) {
            if (v[i] > v[j]) {
                double tmp = v[i];
                v[i] = v[j];
                v[j] = tmp;
            }
        }
    }
}

/** Mescola gli elementi in modo casuale */
void shuffle_vec(double *v, size_t dim) {
    for (size_t i = 0; i < dim; i++) {
        size_t j = (rand() % (dim - i)) + i;
        double tmp = v[i];
        v[i] = v[j];
        v[j] = tmp;
    }
}

/** Shift a destra */
void rshft_vec(double *v, size_t step, size_t dim) {
    for (size_t s = 0; s < step; s++) {
        for (size_t i = dim - 1; i > 0; i--) {
            v[i] = v[i - 1];
        }
        v[0] = 0;
    }
}

/** Shift a sinistra */
void lshft_vec(double *v, size_t step, size_t dim) {
    for (size_t s = 0; s < step; s++) {
        for (size_t i = 0; i < dim - 1; i++) {
            v[i] = v[i + 1];
        }
        v[dim - 1] = 0;
    }
}
/** Rotate a destra: rispetto allo shift gli elementi che escono a destra rientrano in testa (sinistra)*/
void rrot_vec(double *v, size_t step, size_t dim) {
    for (size_t s = 0; s < step; s++) {
        double tmp = v[dim - 1];         // Salva l'ultimo elemento
        for (size_t i = dim - 1; i > 0; i--) {
            v[i] = v[i - 1];             // Sposta ogni elemento a destra
        }
        v[0] = tmp;                      // Inserisci l'elemento salvato in testa
    }
}


void lrot_vec(double *v, size_t step, size_t dim) {
    for (size_t s = 0; s < step; s++) {
        double tmp = v[0];         // salviamo l'ultimo elemento
        for (size_t i = 0; i > dim - 1; i++) {
            v[i] = v[i - 1];             // spostiamo ogni elemento a destra
        }
        v[dim-1] = tmp;                      // inseriamo l'elemento salvato in testa
    }
}

/** Copia n elementi da src a dest (n <= dim) */
void slice_vec(const double *src, double *dest, int start, int n) {
    for (int i = 0; i < n; i++) {
        dest[i] = src[start + i];
    }
}

/** —— Inizializzazione —— */
/** Riempie il vettore con valori casuali in [min, max] */
void rand_vec(int *v, size_t dim, int min, int max) {
    for (size_t i = 0; i < dim; i++) {
        v[i] = min + rand() % (max - min + 1);
    }
}

/** Riempie il vettore con val */
void fill_vec(double *v, size_t dim, double val) {
    for (size_t i = 0; i < dim; i++) {
        v[i] = val;
    }
}

/** Azzera il vettore */
void zero_vec(double *v, size_t dim) {
    fill_vec(v, dim, 0.0);
}

/** —— Norme e geometria —— */
/** Restituisce ||v|| il modulo (norma euclidea) */
double norm_vec(const double *v, size_t dim) {
    double sum = 0.0;
    for (size_t i = 0; i < dim; i++) {
        sum += v[i] * v[i];
    }
    return sqrt(sum);
}

/** —— Statistiche e utilità —— */

/** Restituisce la media degli elementi */
double mean_vec(const double *v, size_t dim) {
    if (dim == 0) return 0.0;
    double sum = 0.0;
    for (size_t i = 0; i < dim; i++) {
        sum += v[i];
    }
    return sum / dim;
}

/** Restituisce il valore minimo */
double min_vec(const double *v, size_t dim) {
    if (dim == 0) return 0.0;
    double min = v[0];
    for (size_t i = 1; i < dim; i++) {
        if (v[i] < min) {
            min = v[i];
        }
    }
    return min;
}

/** Restituisce il valore massimo */
double max_vec(const double *v, size_t dim) {
    if (dim == 0) return 0.0;
    double max = v[0];
    for (size_t i = 1; i < dim; i++) {
        if (v[i] > max) {
            max = v[i];
        }
    }
    return max;
}

/** Somma di tutti gli elementi */
double sum_vec(const double *v, size_t dim) {
    double sum = 0.0;
    for (size_t i = 0; i < dim; i++) {
        sum += v[i];
    }
    return sum;
}

/** Confronta due vettori con tolleranza tol.
    Restituisce true se |v1_i - v2_i| < tol per tutti gli elementi */
bool eq_vec(const double *v1, const double *v2, size_t dim, double tol) {
    for (size_t i = 0; i < dim; i++) {
        if (fabs(v1[i] - v2[i]) >= tol) {
            return false;
        }
    }
    return true;
}

/** Applica func a ogni elemento (modifica v direttamente) */
void map_vec(double *v, size_t dim, double (*func)(double)) {
    for (size_t i = 0; i < dim; i++) {
        v[i] = func(v[i]);
    }
}

/* VECTLIB_H */