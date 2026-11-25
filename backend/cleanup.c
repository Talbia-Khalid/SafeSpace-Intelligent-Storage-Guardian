#include "safespace.h"

#include <dirent.h>
#include <sys/stat.h>
#include <string.h>
#include <stdio.h>

#define LARGE_FILE_SIZE (100LL * 1024 * 1024)

struct CleanupSummary
{
    int empty_files;
    int large_files;
    int temporary_files;
    int inaccessible_paths;

    unsigned long long large_file_bytes;
    unsigned long long temporary_file_bytes;
};

int should_ignore_directory(char name[])
{
    const char *ignored[] = {
        "venv",
        ".venv",
        ".git",
        "__pycache__",
        "node_modules",
        ".idea",
        ".vscode"
    };

    int count = sizeof(ignored) / sizeof(ignored[0]);

    for (int i = 0; i < count; i++)
    {
        if (strcmp(name, ignored[i]) == 0)
            return 1;
    }

    return 0;
}

void scan_cleanup(char path[], struct CleanupSummary *summary)
{
    DIR *dir;
    struct dirent *entry;
    struct stat info;

    dir = opendir(path);

    if (dir == NULL)
    {
        summary->inaccessible_paths++;
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

        int length = snprintf(
            full_path,
            sizeof(full_path),
            "%s/%s",
            path,
            entry->d_name
        );

        if (length < 0 || (size_t)length >= sizeof(full_path))
            continue;

        if (lstat(full_path, &info) != 0)
        {
            summary->inaccessible_paths++;
            continue;
        }

        if (S_ISDIR(info.st_mode))
        {
            if (should_ignore_directory(entry->d_name))
                continue;

            scan_cleanup(full_path, summary);
        }
        else if (S_ISREG(info.st_mode))
        {
            if (info.st_size == 0)
            {
                summary->empty_files++;

                printf("[EMPTY FILE] %s\n", full_path);
            }

            if (info.st_size >= LARGE_FILE_SIZE)
            {
                summary->large_files++;

                summary->large_file_bytes +=
                    (unsigned long long)info.st_size;

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
                    summary->temporary_files++;

                    summary->temporary_file_bytes +=
                        (unsigned long long)info.st_size;

                    printf("[TEMPORARY FILE] %s\n", full_path);
                }
            }
        }
    }

    closedir(dir);
}

void cleanup_recommendations(char path[])
{
    struct CleanupSummary summary = {0};

    printf("\n===== CLEANUP RECOMMENDATIONS =====\n");

    printf("Scanning folder: %s\n\n", path);

    printf("Ignored directories: venv, .git, __pycache__, node_modules and others.\n\n");

    scan_cleanup(path, &summary);

    printf("\n========== SCAN SUMMARY ==========\n");

    printf("Empty files found: %d\n", summary.empty_files);

    printf("Large files found: %d\n", summary.large_files);

    printf("Temporary files found: %d\n", summary.temporary_files);

    printf("Large file storage: %.2f MB\n",
           summary.large_file_bytes / (1024.0 * 1024));

    printf("Temporary file space to review: %.2f MB\n",
           summary.temporary_file_bytes / (1024.0 * 1024));

    printf("Inaccessible paths: %d\n", summary.inaccessible_paths);

    printf("\nNo files have been deleted or modified.\n");

    printf("Review the recommendations before taking any action.\n");

    printf("==================================\n");
}
