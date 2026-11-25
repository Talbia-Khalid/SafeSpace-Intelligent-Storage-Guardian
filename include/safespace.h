#ifndef SAFESPACE_H
#define SAFESPACE_H

#include <stdio.h>
#include <sys/statvfs.h>

void check_storage();
void analyze_directory(char path[]);
void detect_duplicates(char path[]);
void get_duplicate_summary(
    char path[],
    int *duplicate_pairs,
    unsigned long long *saved_size
);

void save_storage_history(
    unsigned long long total,
    unsigned long long used,
    unsigned long long available,
    double percentage
);

void show_storage_history();
void monitor_directory(char path[]);
void vault_menu();
void quarantine_file(char path[]);
void list_quarantined_files();
void restore_file(int id);

void cleanup_recommendations(char path[]);

void emergency_mode(char path[]);

void storage_health_score();

void generate_storage_report(char path[]);

#endif
