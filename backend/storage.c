#include "safespace.h"

void check_storage()
{
    struct statvfs disk;

    if (statvfs("/", &disk) != 0)
    {
        printf("Error checking storage!\n");
        return;
    }

    unsigned long long total;
    unsigned long long free_space;
    unsigned long long used;

    total = (unsigned long long)disk.f_blocks * disk.f_frsize;

    free_space = (unsigned long long)disk.f_bavail * disk.f_frsize;

    used = total - ((unsigned long long)disk.f_bfree * disk.f_frsize);

    double percentage;

    percentage = (double)used / total * 100;

    printf("\n===== STORAGE INFORMATION =====\n");

    printf("Total Storage: %.2f GB\n", total / (1024.0 * 1024 * 1024));

    printf("Used Storage: %.2f GB\n", used / (1024.0 * 1024 * 1024));

    printf("Available Storage: %.2f GB\n", free_space / (1024.0 * 1024 * 1024));

    printf("Storage Usage: %.2f%%\n", percentage);

    if (percentage >= 90)
    {
        printf("WARNING: Storage is almost full!\n");
    }
    else if (percentage >= 75)
    {
        printf("NOTICE: Storage usage is getting high.\n");
    }
    else
    {
        printf("Storage condition is normal.\n");
    }

    printf("================================\n");
    save_storage_history(total, used, free_space, percentage);
}
