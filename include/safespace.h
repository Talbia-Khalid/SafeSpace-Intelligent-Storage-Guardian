#ifndef SAFESPACE_H
#define SAFESPACE_H

#include <stdio.h>
#include <sys/statvfs.h>

void check_storage();
void analyze_directory(char path[]);
void detect_duplicates(char path[]);

void save_storage_history(
    unsigned long long total,
    unsigned long long used,
    unsigned long long available,
    double percentage
);

void show_storage_history();

#endif
