#ifndef UTILS_H
#define UTILS_H

#include <stdio.h>

typedef struct FileRecord {
    FILE *fp;           
    int index;          
    int handle;         
} FileRecord;

typedef struct OpenInfo {
    int tot_opens;              
    int failed_opens;           
    FileRecord *records;        
    int records_size;           
} OpenInfo;

void init_open_info(OpenInfo *info);
int add_file_record(OpenInfo *info, FILE *fp);
void close_all_files(OpenInfo *info);
void print_report(const OpenInfo *info);
void cleanup_open_info(OpenInfo *info);

#endif // UTILS_H