#ifndef FLOAT_LIB_H
#define FLOAT_LIB_H

#include <stdint.h>
#include <stdio.h>

// Float (32-bit) functions
void float_to_esp(float n);
void esp_to_float(int s, int e, uint32_t m);

// Double (64-bit) functions
void double_to_esp(double n);
void esp_to_double(int s, int e, uint64_t m);

// Half-precision (16-bit) functions
void half_to_esp(uint16_t n);
void esp_to_half(int s, int e, uint16_t m);

#endif // FLOAT_LIB_H
