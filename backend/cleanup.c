
#include "safespace.h"

#include <dirent.h>
#include <sys/stat.h>
#include <string.h>
#include <stdio.h>

#define LARGE_FILE_SIZE (100LL * 1024 * 1024)

void scan_cleanup(char path[])
{
    DIR *dir;
    struct dirent *entry;
    struct stat info;

    dir = opendir(path);

    if (dir == NULL)
        return;

    while ((entry = readdir(dir)) != NULL)
    {
        if (strcmp(entry->d_name, ".") == 0 ||
            strcmp(entry->d_name, "..") == 0)
        {
            continue;
        }

        char full_path[1024];

        int length = snprintf(full_path, sizeof(full_path),
                             "%s/%s", path, entry->d_name);

        if (length < 0 || length >= sizeof(full_path))
            continue;

        if (lstat(full_path, &info) != 0)
            continue;

        if (S_ISDIR(info.st_mode))
        {
            scan_cleanup(full_path);
        }
        else if (S_ISREG(info.st_mode))
        {
            if (info.st_size == 0)
            {
                printf("[EMPTY FILE] %s\n", full_path);
            }

            if (info.st_size >= LARGE_FILE_SIZE)
            {
                printf("[LARGE FILE] %s (%.2f MB)\n",
                       full_path,
                       info.st_size / (1024.0 * 1024));
            }

            char *extension = strrchr(entry->d_name, '.');

            if (extension != NULL)
            {
                if (strcmp(extension, ".tmp") == 0 ||
                    strcmp(extension, ".temp") == 0 ||
                    strcmp(extension, ".cache") == 0)
                {
                    printf("[TEMPORARY FILE] %s\n",
                           full_path);
                }
            }
        }
    }

    closedir(dir);
}

void cleanup_recommendations(char path[])
{
    printf("\n===== CLEANUP RECOMMENDATIONS =====\n");

    printf("Scanning folder: %s\n\n", path);

    scan_cleanup(path);

    printf("\n===== SCAN COMPLETED =====\n");
    printf("No files have been deleted or modified.\n");
}

