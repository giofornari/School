#include <stdio.h>
#include <stdint.h>
#include <math.h>
#include "float_lib.h"
void float_to_esp(float n) {
    uint32_t tmp = *(uint32_t*)&n; // puntatore casting ((uint32_t*)&n) per n a uint32_t (bit a bit)

    int s = - 2 * ((tmp >> 31) & 1) +1; 
    int e = ((tmp >> 23) & 0xFF) - 127; // estrazione esp e rm di bias
    uint32_t m = tmp & 0x007FFFFF;     
    // frac è numero + 1 pk normalizzato 
    double frac = 1.0 + ((double)m / (1 << 23)); // converte in una frazione decimale

    double value = s * frac * pow(2, e); // ret al num

    printf("Float: %d * %.10f * 2^%d = %.10f\n", s, frac, e, value);
}

void double_to_esp(double n) { // 8 byte 64 bit
    uint64_t bits = *(uint64_t*)&n; 

    int s = -2 * ((bits >> 63) & 1) +1;
    int e = ((bits >> 52) & 0x7FF) - 1023; // bias 1023
    uint64_t m = bits & 0x000FFFFFFFFFFFFF; // mascheramento

    double frac = 1.0 + ((double)m / (1ULL << 52)); // conv in dec frac 0.?????
    double value = s * frac * pow(2, e); // ret

    printf("Double: %d * %.16f * 2^%d = %.16f\n", s, frac, e, value);
}

void esp_to_float(int s, int e, uint32_t m) {
    uint32_t tmp = ((s < 0) << 31) | ((e + 127) << 23) | (m & 0x007FFFFF);
    float result = *(float*)&tmp;
    printf("virgola mobile to Float: %d * %f * 2^%d = %f\n", s, 1.0 + ((double)m / (1 << 23)), e, result);
}

void esp_to_double(int s, int e, uint64_t m) {
    uint64_t bits = ((uint64_t)(s < 0) << 63) | ((uint64_t)(e + 1023) << 52) | (m & 0x000FFFFFFFFFFFFF);
    double result = *(double*)&bits;
    printf("virgola mobile to Double: %d * %f * 2^%d = %f\n", s, 1.0 + ((double)m / (1ULL << 52)), e, result);
}

void half_to_esp(uint16_t n) {
    int s = -2 * ((n >> 15) & 1) + 1;
    int e = ((n >> 10) & 0x1F) - 15;
    uint16_t m = n & 0x03FF;
    double frac = 1.0 + ((double)m / (1 << 10));
    double value = s * frac * pow(2, e);
    printf("Half: %d * %.10f * 2^%d = %.10f\n", s, frac, e, value);
}

void esp_to_half(int s, int e, uint16_t m) {
    uint16_t result = ((s < 0) << 15) | ((e + 15) << 10) | (m & 0x03FF);
    printf("virgola mobile to Half: segno=%d, espo=%d, mantissa=%d -> Half=0x%04X\n", s, e, m, result);
}

