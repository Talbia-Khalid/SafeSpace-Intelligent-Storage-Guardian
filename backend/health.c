
#include "safespace.h"
#include <sys/statvfs.h>

void storage_health_score()
{
    struct statvfs disk;

    if (statvfs("/", &disk) != 0)
    {
        printf("\nUnable to calculate storage health score.\n");
        return;
    }

    unsigned long long total =
        (unsigned long long)disk.f_blocks * disk.f_frsize;

    unsigned long long free_space =
        (unsigned long long)disk.f_bavail * disk.f_frsize;

    if (total == 0)
    {
        printf("Storage information is invalid.\n");
        return;
    }

    unsigned long long used = total - free_space;

    double percentage = (double)used / total * 100;

    int score;

    if (percentage < 70)
        score = 100;
    else if (percentage < 85)
        score = 80;
    else if (percentage < 95)
        score = 60;
    else
        score = 30;

    printf("\n===== SAFESPACE HEALTH SCORE =====\n");

    printf("System Storage Usage: %.2f%%\n", percentage);

    printf("Storage Health Score: %d/100\n", score);

    if (score >= 80)
        printf("Storage Health: GOOD\n");
    else if (score >= 60)
        printf("Storage Health: MODERATE\n");
    else
        printf("Storage Health: POOR\n");

    printf("=================================\n");
}

