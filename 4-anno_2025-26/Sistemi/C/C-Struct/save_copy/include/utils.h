/**
 * @file utils.h
 * @author giordii (admin@giordii.dev)
 * @brief Header file for safe_copy utility functions
 * @version 0.1
 * @date 2025-12-04
 * 
 * @copyright Copyright (c) 2025
 * 
 */

#ifndef UTILS_H
#define UTILS_H

#include <stddef.h>
#include <stdbool.h>

/**
 * @brief Struct to track copy operation statistics
 */
typedef struct CopyStats {
    size_t bytes_copied;      // Total number of bytes successfully copied
    size_t read_errors;       // Number of read errors encountered
    size_t write_errors;      // Number of write errors encountered
} CopyStats;

/**
 * @brief Safely copies a file from source to destination
 * 
 * @param source Path to source file
 * @param dest Path to destination file
 * @param stats Pointer to CopyStats struct to track operation
 * @return int 0 on success, -1 on failure
 */
int safe_copy(const char *source, const char *dest, CopyStats *stats);

/**
 * @brief Prints copy statistics to stdout
 * 
 * @param stats Pointer to CopyStats struct
 */
void print_stats(const CopyStats *stats);

#endif // UTILS_H