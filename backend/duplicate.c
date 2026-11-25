#include "safespace.h"
#include <openssl/evp.h>
#include <dirent.h>
#include <sys/stat.h>
#include <string.h>
#include <stdlib.h>

#define MAX_FILES 1000

struct FileData
{
    char path[1024];
    char hash[65];
    unsigned long long size;
};

struct FileData files[MAX_FILES];

int file_total = 0;

int should_skip_directory(char name[])
{
    if (strcmp(name, ".git") == 0 ||
        strcmp(name, "venv") == 0 ||
        strcmp(name, ".venv") == 0 ||
        strcmp(name, "__pycache__") == 0 ||
        strcmp(name, "node_modules") == 0)
    {
        return 1;
    }

    return 0;
}

void calculate_hash(char path[], char hash[])
{
    FILE *file;
    unsigned char buffer[4096];
    unsigned char digest[EVP_MAX_MD_SIZE];

    unsigned int length = 0;
    size_t bytes;

    hash[0] = '\0';

    file = fopen(path, "rb");

    if (file == NULL)
        return;

    EVP_MD_CTX *context = EVP_MD_CTX_new();

    if (context == NULL)
    {
        fclose(file);
        return;
    }

    if (EVP_DigestInit_ex(context, EVP_sha256(), NULL) != 1)
    {
        EVP_MD_CTX_free(context);
        fclose(file);
        return;
    }

    while ((bytes = fread(buffer, 1, sizeof(buffer), file)) > 0)
    {
        if (EVP_DigestUpdate(context, buffer, bytes) != 1)
        {
            EVP_MD_CTX_free(context);
            fclose(file);
            return;
        }
    }

    if (ferror(file))
    {
        EVP_MD_CTX_free(context);
        fclose(file);
        return;
    }

    if (EVP_DigestFinal_ex(context, digest, &length) != 1)
    {
        EVP_MD_CTX_free(context);
        fclose(file);
        return;
    }

    for (unsigned int i = 0; i < length; i++)
    {
        sprintf(hash + (i * 2), "%02x", digest[i]);
    }

    hash[length * 2] = '\0';

    fclose(file);
    EVP_MD_CTX_free(context);
}

void scan_files(char path[])
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
            continue;

        if (S_ISDIR(info.st_mode))
        {
            if (should_skip_directory(entry->d_name))
                continue;

            scan_files(full_path);
        }
        else if (S_ISREG(info.st_mode) && info.st_size > 0)
        {
            if (file_total >= MAX_FILES)
                continue;

            snprintf(
                files[file_total].path,
                sizeof(files[file_total].path),
                "%s",
                full_path
            );

            files[file_total].size =
                (unsigned long long)info.st_size;

            calculate_hash(
                full_path,
                files[file_total].hash
            );

            if (files[file_total].hash[0] != '\0')
            {
                file_total++;
            }
        }
    }

    closedir(dir);
}

/* Calculate duplicate information for Emergency Mode */
void get_duplicate_summary(
    char path[],
    int *duplicate_pairs,
    unsigned long long *saved_size
)
{
    file_total = 0;

    *duplicate_pairs = 0;
    *saved_size = 0;

    scan_files(path);

    for (int i = 0; i < file_total; i++)
    {
        int has_earlier_match = 0;

        for (int j = 0; j < i; j++)
        {
            if (strcmp(files[i].hash, files[j].hash) == 0)
            {
                has_earlier_match = 1;
                break;
            }
        }

        for (int j = i + 1; j < file_total; j++)
        {
            if (strcmp(files[i].hash, files[j].hash) == 0)
            {
                (*duplicate_pairs)++;
            }
        }

        if (has_earlier_match)
        {
            *saved_size += files[i].size;
        }
    }
}

/* Normal duplicate detector */
void detect_duplicates(char path[])
{
    file_total = 0;

    printf("\nScanning files for duplicates...\n");
    printf("Ignored directories: venv, .git, __pycache__ and others.\n");

    scan_files(path);

    int duplicate_count = 0;
    unsigned long long saved_size = 0;

    printf("\n===== DUPLICATE FILES =====\n");

    for (int i = 0; i < file_total; i++)
    {
        int has_earlier_match = 0;

        for (int j = 0; j < i; j++)
        {
            if (strcmp(files[i].hash, files[j].hash) == 0)
            {
                has_earlier_match = 1;
                break;
            }
        }

        for (int j = i + 1; j < file_total; j++)
        {
            if (strcmp(files[i].hash, files[j].hash) == 0)
            {
                printf("\nDuplicate Found:\n");
                printf("File 1: %s\n", files[i].path);
                printf("File 2: %s\n", files[j].path);

                duplicate_count++;
            }
        }

        if (has_earlier_match)
        {
            saved_size += files[i].size;
        }
    }

    if (duplicate_count == 0)
    {
        printf("No duplicate files found.\n");
    }

    printf("\nTotal Files Scanned: %d\n", file_total);
    printf("Total Duplicate Pairs: %d\n", duplicate_count);

    printf("Potential Storage Savings: %.2f MB\n",
           saved_size / (1024.0 * 1024));

    printf("===========================\n");
}
