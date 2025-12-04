#ifndef CLASSIFIER_H
#define CLASSIFIER_H

#include "ip_types.h"
#include <stdint.h>

char classify_ip(uint32_t ip);
IPType get_ip_type(uint32_t ip);
const char* ip_type_to_string(IPType type);
bool is_valid_host_ip(uint32_t ip, uint32_t network, uint32_t broadcast);

#endif
