#ifndef GENERATOR_H
#define GENERATOR_H

#include "ip_types.h"
#include "ipset.h"
#include <stdint.h>
#include <stdbool.h>

void init_random_generator(void);
uint32_t random_range(uint32_t min, uint32_t max);
uint32_t generate_random_ip(void);
uint32_t generate_ip_by_class(char class_filter);
uint32_t generate_ip_in_cidr(uint32_t network, uint8_t prefix_len, 
                             int max_attempts, bool *success);
uint32_t generate_ip_in_range(uint32_t start_ip, uint32_t end_ip);
int generate_unique_ips(const ProgramOptions *opts, IPAddress *output);
bool check_generation_feasibility(const ProgramOptions *opts);

#endif
