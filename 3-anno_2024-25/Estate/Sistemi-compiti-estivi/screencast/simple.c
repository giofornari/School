/* mem_demo.c
   Dimostrazione di allocazioni: .text, .rodata, .data, .bss, stack, heap
   Compilare: gcc -O0 -fno-pie -no-pie -g mem_demo.c -o mem_demo
   (se la tua toolchain non supporta -no-pie, rimuovili; vedrai comunque indirizzi ma con ASLR attivo)
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

/* ---------- GLOBALI (segmenti .data / .bss / .rodata) ---------- */

/* string literal: nel .rodata */
const char *APP_NAME = "MemDemo v1.0";

/* globali inizializzate: .data */
int global_counter = 42;
double global_threshold = 3.14;

/* globali non inizializzate: .bss */
long uninitialized_global_long;    /* vale 0 all'avvio (bss) */
char *last_allocated = NULL;       /* puntatore globale (bss) */

/* ---------- TIPI ---------- */

typedef struct {
    int id;
    char *name;      /* puntatore a stringa (heap o literal) */
    float score;
} Record;

/* ---------- FUNZIONI ---------- */

/* crea record su heap e ritorna puntatore */
Record *create_record(int id, const char *name, float score) {
    Record *r = malloc(sizeof(Record));
    if (!r) { perror("malloc"); exit(1); }
    r->id = id;
    /* duplico la stringa su heap */
    size_t n = strlen(name) + 1;
    r->name = malloc(n);
    if (!r->name) { perror("malloc"); exit(1); }
    memcpy(r->name, name, n);
    r->score = score;
    return r;
}

/* manipola (espande) una stringa con realloc */
char *append_exclamation(char *s) {
    size_t old = strlen(s);
    char *t = realloc(s, old + 3); /* spazio per '!!' e '\0' */
    if (!t) { perror("realloc"); exit(1); }
    strcat(t, "!!");
    return t;
}

/* stampa bit di un unsigned int (32-bit) per esercizio */
void print_binary32(uint32_t v) {
    for (int i = 31; i >= 0; --i) {
        putchar(((v >> i) & 1) ? '1' : '0');
        if (i % 8 == 0 && i != 0) putchar('.');
    }
    putchar('\n');
}

/* funzione che mostra indirizzi e contenuto */
void show_addresses(Record *r_arr[], int n,
                    char *dyn_buf, size_t dyn_buf_size) {
    printf("\n--- Address snapshot ---\n");
    printf("Function 'create_record' (text): %p\n", (void*)create_record);
    printf("APP_NAME (rodata ptr): %p -> \"%s\"\n", (void*)&APP_NAME, APP_NAME);
    printf("global_counter (data): %p -> %d\n", (void*)&global_counter, global_counter);
    printf("global_threshold (data): %p -> %f\n", (void*)&global_threshold, global_threshold);
    printf("uninitialized_global_long (bss): %p -> %ld\n", (void*)&uninitialized_global_long, uninitialized_global_long);
    printf("last_allocated (bss): %p -> %p\n", (void*)&last_allocated, (void*)last_allocated);

    printf("\n-- Stack local addresses --\n");
    int stack_local = 12345;
    printf("&stack_local: %p (value=%d)\n", (void*)&stack_local, stack_local);

    for (int i = 0; i < n; ++i) {
        Record *r = r_arr[i];
        printf("\nRecord[%d] struct addr (stack array element pointer): %p\n", i, (void*)&r_arr[i]);
        printf(" -> pointee Record* value: %p\n", (void*)r);
        if (r) {
            printf("    record struct at %p: id=%d score=%f name_ptr=%p\n", (void*)r, r->id, r->score, (void*)r->name);
            if (r->name) printf("    name content: \"%s\"\n", r->name);
        } else {
            printf("    (NULL)\n");
        }
    }
    printf("\nHeap dynamic buffer: ptr=%p size=%zu content=\"%s\"\n", (void*)dyn_buf, dyn_buf_size, dyn_buf ? dyn_buf : "(null)");
    last_allocated = dyn_buf; /* salviamo l'ultimo allocato in globale per esercizio */
    printf("--- end snapshot ---\n\n");
}

/* ---------- main: usa stack, heap, globali, static locali ---------- */

int main(void) {
    printf("=== %s ===\n", APP_NAME);

    /* variabili automatiche (stack) */
    const int N = 3;
    Record *records[N];       /* array statico sullo stack: contiene 3 puntatori (automatici) */
    for (int i = 0; i < N; ++i) records[i] = NULL;

    /* buffer dinamico con malloc */
    char *dyn = malloc(32);
    if (!dyn) { perror("malloc"); return 1; }
    strcpy(dyn, "hello");
    dyn = append_exclamation(dyn); /* usa realloc internamente */

    /* creo 2 record su heap */
    records[0] = create_record(1, "Alice", 9.5f);
    records[1] = create_record(2, "Bob", 7.25f);
    /* lasciamo records[2] NULL per mostrare valore in stack */

    /* stampo valori & indirizzi */
    show_addresses(records, N, dyn, strlen(dyn));

    /* manipolazioni: libero il primo record parzialmente */
    free(records[0]->name); /* libero il nome */
    free(records[0]);       /* libero il struct */
    records[0] = NULL;

    /* uso calloc per un piccolo array di int (heap) */
    int *arr = calloc(5, sizeof(int));
    if (!arr) { perror("calloc"); return 1; }
    for (int i = 0; i < 5; ++i) arr[i] = i * 10;

    printf("arr (calloc) at %p, arr[3]=%d\n", (void*)arr, arr[3]);

    /* ridimensiono arr con realloc */
    int *arr2 = realloc(arr, 10 * sizeof(int)); /* ora 10 elementi */
    if (!arr2) { perror("realloc"); free(arr); return 1; }
    arr = arr2;
    arr[5] = 555;

    printf("after realloc arr at %p arr[5]=%d\n", (void*)arr, arr[5]);

    /* snapshot finale */
    show_addresses(records, N, dyn, strlen(dyn));

    /* liberiamo risorse: liberiamo tutto tranne l'ultimo nome per dimostrare come si verifica un leak (se voluto) */
    if (records[1]) {
        free(records[1]->name);
        free(records[1]);
        records[1] = NULL;
    }
    free(arr);
    free(dyn);
    /* last_allocated ora punta a dyn (che abbiamo appena freed) -> dangling pointer globale! */
    printf("last_allocated (globale) ora contiene (dangling) = %p\n", (void*)last_allocated);

    return 0;
}
