#include "safespace.h"
#include <sys/statvfs.h>

void emergency_mode(char path[])
{
    struct statvfs disk;

    if (statvfs("/", &disk) != 0)
    {
        printf("\nUnable to check system storage.\n");
        return;
    }

    unsigned long long total;
    unsigned long long free_space;
    unsigned long long used;

    total = (unsigned long long)disk.f_blocks * disk.f_frsize;

    free_space = (unsigned long long)disk.f_bavail * disk.f_frsize;

    used = total - ((unsigned long long)disk.f_bfree * disk.f_frsize);

    double percentage = (double)used / total * 100;

    printf("\n========== EMERGENCY MODE ==========\n");

    printf("Storage Usage: %.2f%%\n", percentage);

    printf("Available Space: %.2f GB\n",
           free_space / (1024.0 * 1024 * 1024));

    if (percentage >= 95)
    {
        printf("\n!!! CRITICAL STORAGE WARNING !!!\n");
        printf("Your system storage is almost full!\n");

        printf("\nRecommended Actions:\n");
        printf("1. Review large files.\n");
        printf("2. Check duplicate files.\n");
        printf("3. Review temporary files.\n");
        printf("4. Check your Downloads folder.\n");

        printf("\nScanning for files that may need attention...\n");

        cleanup_recommendations(path);
    }
    else if (percentage >= 85)
    {
        printf("\nWARNING: Storage usage is very high!\n");
        printf("Consider reviewing unnecessary files.\n");

        printf("\nScanning for cleanup recommendations...\n");

        cleanup_recommendations(path);
    }
    else if (percentage >= 70)
    {
        printf("\nNOTICE: Storage usage is increasing.\n");
        printf("Consider checking large files.\n");
    }
    else
    {
        printf("\nStorage condition is normal.\n");
        printf("Emergency Mode is not required right now.\n");
    }

    printf("\n==================================\n");
}
