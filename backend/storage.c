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

    printf("\n===== STORAGE INFORMATION =====\n");

    printf("Total Storage: %.2f GB\n", total / (1024.0 * 1024 * 1024));

    printf("Used Storage: %.2f GB\n", used / (1024.0 * 1024 * 1024));

    printf("Available Storage: %.2f GB\n", free_space / (1024.0 * 1024 * 1024));

    printf("================================\n");
}
