#include "safespace.h"
#include <dirent.h>
#include <sys/stat.h>
#include <string.h>

unsigned long long total_size = 0;
int file_count = 0;
int folder_count = 0;

void scan_directory(char path[])
{
    DIR *dir;
    struct dirent *entry;
    struct stat info;

    dir = opendir(path);

    if (dir == NULL)
    {
        printf("Cannot open folder: %s\n", path);
        return;
    }

    while ((entry = readdir(dir)) != NULL)
    {
        if (strcmp(entry->d_name, ".") == 0 ||
            strcmp(entry->d_name, "..") == 0)
        {
            continue;
        }

        char full_path[1024];

        snprintf(full_path, sizeof(full_path), "%s/%s",
                 path, entry->d_name);

        if (lstat(full_path, &info) != 0)
        {
            continue;
        }

        if (S_ISDIR(info.st_mode))
        {
            folder_count++;
            scan_directory(full_path);
        }
        else if (S_ISREG(info.st_mode))
        {
            file_count++;
            total_size += info.st_size;
        }
    }

    closedir(dir);
}

void analyze_directory(char path[])
{
    total_size = 0;
    file_count = 0;
    folder_count = 0;

    printf("\nScanning folder...\n");

    scan_directory(path);

    printf("\n===== DIRECTORY ANALYSIS =====\n");

    printf("Folder: %s\n", path);
    printf("Total Files: %d\n", file_count);
    printf("Total Subfolders: %d\n", folder_count);

    printf("Total Size: %.2f MB\n",
           total_size / (1024.0 * 1024));

    printf("================================\n");
}
