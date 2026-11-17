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
};

struct FileData files[MAX_FILES];

int file_total = 0;

void calculate_hash(char path[], char hash[])
{
    FILE *file;
    unsigned char buffer[4096];
    unsigned char digest[EVP_MAX_MD_SIZE];

    unsigned int length = 0;

    EVP_MD_CTX *context = EVP_MD_CTX_new();

    if (context == NULL)
        return;

    file = fopen(path, "rb");

    if (file == NULL)
    {
        EVP_MD_CTX_free(context);
        return;
    }

    EVP_DigestInit_ex(context, EVP_sha256(), NULL);

    size_t bytes;

    while ((bytes = fread(buffer, 1, sizeof(buffer), file)) > 0)
    {
        EVP_DigestUpdate(context, buffer, bytes);
    }

    EVP_DigestFinal_ex(context, digest, &length);

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

        snprintf(full_path, sizeof(full_path),
                 "%s/%s", path, entry->d_name);

        if (lstat(full_path, &info) != 0)
            continue;

        if (S_ISDIR(info.st_mode))
        {
            scan_files(full_path);
        }
        else if (S_ISREG(info.st_mode))
        {
            if (file_total >= MAX_FILES)
                continue;

            strcpy(files[file_total].path, full_path);

            calculate_hash(full_path, files[file_total].hash);

            if (files[file_total].hash[0] != '\0')
                file_total++;
        }
    }

    closedir(dir);
}

void detect_duplicates(char path[])
{
    file_total = 0;

    printf("\nScanning files for duplicates...\n");

    scan_files(path);

    int duplicate_count = 0;

    printf("\n===== DUPLICATE FILES =====\n");

    for (int i = 0; i < file_total; i++)
    {
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
    }

    if (duplicate_count == 0)
    {
        printf("No duplicate files found.\n");
    }

    printf("\nTotal duplicate pairs: %d\n", duplicate_count);
    printf("===========================\n");
}
