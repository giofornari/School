#ifndef PARSER_H
#define PARSER_H

#include "ip_types.h"
#include <stdbool.h>
#include <stdint.h>

bool parse_cidr(const char *cidr_str, uint32_t *network, uint8_t *prefix_len);
bool parse_range(const char *range_str, uint32_t *start_ip, uint32_t *end_ip);
bool parse_arguments(int argc, char *argv[], ProgramOptions *opts);
void print_usage(const char *program_name);
bool validate_options(const ProgramOptions *opts);

#endif
