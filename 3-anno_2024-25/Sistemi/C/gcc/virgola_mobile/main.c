#include "float_lib.h"
#include <stdio.h>

int main() {
    // Example usage
    float f = 3.14f;
    double d = 2.71828;
    uint16_t h = 0x3C00;  // 1.0 in half-precision

    printf("--- Float Conversion ---\n");
    float_to_esp(f);
    esp_to_float(1, 0, 0x400000);

    printf("\n--- Double Conversion ---\n");
    double_to_esp(d);
    esp_to_double(1, 1, 0x8000000000000);

    printf("\n--- Half Precision Conversion ---\n");
    half_to_esp(h);
    esp_to_half(1, 0, 0x200);
    return 0;
}
