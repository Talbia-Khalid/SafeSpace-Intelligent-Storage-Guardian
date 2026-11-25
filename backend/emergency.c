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

    struct CleanupSummary cleanup = {0};

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

    if (percentage < 70)
    {
        printf("\nEmergency assessment is not required.\n");
        printf("\n========================================\n");
        return;
    }

    printf("\nSTARTING GUARDIAN ASSESSMENT...\n");

    /* CLEANUP ASSESSMENT */

    printf("\n[1] CLEANUP ANALYSIS\n");

    printf("Scanning selected folder: %s\n", path);

    get_cleanup_summary(path, &cleanup);

    printf("\nCleanup Findings:\n");
    printf("Empty files: %d\n", cleanup.empty_files);
    printf("Large files: %d\n", cleanup.large_files);
    printf("Temporary files: %d\n", cleanup.temporary_files);

    printf("Temporary space to review: %.2f MB\n",
           cleanup.temporary_file_bytes / (1024.0 * 1024));

    /* DUPLICATE ASSESSMENT */

    printf("\n[2] DUPLICATE ANALYSIS\n");

    get_duplicate_summary(
        path,
        &duplicate_pairs,
        &duplicate_savings
    );

    printf("Duplicate pairs found: %d\n", duplicate_pairs);

    printf("Potential duplicate savings: %.2f MB\n",
           duplicate_savings / (1024.0 * 1024));

    /* GUARDIAN RECOMMENDATIONS */

    printf("\n[3] INTELLIGENT GUARDIAN RECOMMENDATIONS\n");

    if (percentage >= 95)
    {
        printf("[CRITICAL] System storage is almost full.\n");
        printf("Review storage immediately.\n");
    }
    else if (percentage >= 85)
    {
        printf("[HIGH] Storage usage is very high.\n");
        printf("Prioritize reviewing unnecessary files.\n");
    }

    if (duplicate_pairs > 0)
    {
        printf("[MEDIUM] Duplicate files detected.\n");
        printf("Review duplicate files to identify possible savings.\n");
    }

    if (cleanup.temporary_files > 0)
    {
        printf("[MEDIUM] Temporary files detected.\n");
        printf("Review them before removing anything.\n");
    }

    if (cleanup.empty_files > 0)
    {
        printf("[LOW] Empty files detected.\n");
        printf("Check whether these files are still needed.\n");
    }

    if (cleanup.large_files > 0)
    {
        printf("[LOW] Large files detected.\n");
        printf("Review their purpose before taking action.\n");
    }

    if (duplicate_pairs == 0 &&
        cleanup.temporary_files == 0 &&
        cleanup.empty_files == 0 &&
        cleanup.large_files == 0 &&
        percentage < 85)
    {
        printf("No significant cleanup concerns were detected.\n");
    }

    printf("\n========================================\n");
    printf("       GUARDIAN ASSESSMENT COMPLETE\n");
    printf("========================================\n");

    printf("No files have been deleted or modified.\n");
    printf("All recommendations require user review.\n");
}
