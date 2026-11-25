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

    unsigned long long total =
        (unsigned long long)disk.f_blocks * disk.f_frsize;

    unsigned long long free_space =
        (unsigned long long)disk.f_bavail * disk.f_frsize;

    unsigned long long used =
        total - ((unsigned long long)disk.f_bfree * disk.f_frsize);

    double percentage = (double)used / total * 100;

    int duplicate_pairs = 0;
    unsigned long long duplicate_savings = 0;

    printf("\n========================================\n");
    printf("        SAFESPACE EMERGENCY MODE\n");
    printf("========================================\n");

    printf("\nSYSTEM STORAGE ASSESSMENT\n");

    printf("Storage Usage: %.2f%%\n", percentage);

    printf("Available Space: %.2f GB\n",
           free_space / (1024.0 * 1024 * 1024));

    if (percentage >= 95)
    {
        printf("\nRISK LEVEL: CRITICAL\n");
        printf("Immediate storage attention is required.\n");
    }
    else if (percentage >= 85)
    {
        printf("\nRISK LEVEL: HIGH\n");
        printf("System storage is running low.\n");
    }
    else if (percentage >= 70)
    {
        printf("\nRISK LEVEL: NOTICE\n");
        printf("Storage usage is increasing.\n");
    }
    else
    {
        printf("\nRISK LEVEL: NORMAL\n");
        printf("System storage condition is healthy.\n");
    }

    printf("\n========================================\n");

    if (percentage >= 70)
    {
        printf("\nSTARTING GUARDIAN ASSESSMENT...\n");

        printf("\n[1] CLEANUP ANALYSIS\n");

        cleanup_recommendations(path);

        printf("\n[2] DUPLICATE ANALYSIS\n");

        get_duplicate_summary(
            path,
            &duplicate_pairs,
            &duplicate_savings
        );

        printf("Duplicate pairs found: %d\n", duplicate_pairs);

        printf("Potential duplicate savings: %.2f MB\n",
               duplicate_savings / (1024.0 * 1024));

        printf("\n[3] GUARDIAN RECOMMENDATIONS\n");

        if (duplicate_pairs > 0)
        {
            printf("[HIGH PRIORITY] Review duplicate files.\n");
        }

        printf("[REVIEW] Check temporary files before removing them.\n");

        printf("[REVIEW] Inspect large files before taking action.\n");

        if (percentage >= 95)
        {
            printf("[CRITICAL] Free up storage space as soon as possible.\n");
        }
        else if (percentage >= 85)
        {
            printf("[WARNING] Monitor storage and review cleanup options.\n");
        }
        else
        {
            printf("[NOTICE] Continue monitoring storage growth.\n");
        }
    }
    else
    {
        printf("\nEmergency assessment is not required.\n");
    }

    printf("\n========================================\n");
    printf("       GUARDIAN ASSESSMENT COMPLETE\n");
    printf("========================================\n");

    printf("No files have been deleted or modified.\n");
    printf("All recommendations require user review.\n");
}
