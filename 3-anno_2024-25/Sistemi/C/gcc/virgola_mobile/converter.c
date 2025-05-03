#include <stdio.h>
#include <stdint.h>

void float_to_esp(float n) {
    int s = -2* ((unsigned int)n >> 31)+1;
    int e = ((unsigned int) n >> 23) & 0xff;
    // e = e - 127;
    unsigned int m = (unsigned int) n & 0x007fffff;
    printf("%d *  1.%u * 2^%d\n", s, m, e);
}
void double_to_esp(double n) {
    int s = -2* ((unsigned long long)n >> 63)+1;
    int e = (((long long) n >> 52) & 0x7FF); // - 1023;
    unsigned long long m = (unsigned long long) n & 0x000FFFFFFFFFFFFF;

    printf("%d * 1.%llu * 2^%d\n", s, m, e);
}

int main() {
    float n = 0;
    scanf("%f", &n);
    float_to_esp(n);
    double m = 0;
    scanf("%lf", &m);
    double_to_esp(m);
}