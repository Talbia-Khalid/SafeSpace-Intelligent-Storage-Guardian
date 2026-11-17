#include "safespace.h"

#include <sqlite3.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <errno.h>

int open_vault_database(sqlite3 **db)
{
    int result = sqlite3_open("database/safespace.db", db);

    if (result != SQLITE_OK)
    {
        printf("Database connection failed!\n");
        sqlite3_close(*db);
        return 0;
    }

    char *query =
        "CREATE TABLE IF NOT EXISTS quarantine ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "original_path TEXT NOT NULL,"
        "vault_path TEXT NOT NULL,"
        "status TEXT DEFAULT 'quarantined',"
        "quarantined_at DATETIME DEFAULT CURRENT_TIMESTAMP"
        ");";

    result = sqlite3_exec(*db, query, NULL, NULL, NULL);

    if (result != SQLITE_OK)
    {
        printf("Could not create quarantine table!\n");
        sqlite3_close(*db);
        return 0;
    }

    return 1;
}

void quarantine_file(char path[])
{
    struct stat info;

    if (lstat(path, &info) != 0)
    {
        printf("File does not exist!\n");
        return;
    }

    if (!S_ISREG(info.st_mode))
    {
        printf("Only regular files can be quarantined!\n");
        return;
    }

    char choice[20];

    printf("\nAre you sure you want to quarantine this file? (y/n): ");

    if (fgets(choice, sizeof(choice), stdin) == NULL)
        return;

    if (choice[0] != 'y' && choice[0] != 'Y')
    {
        printf("Quarantine cancelled.\n");
        return;
    }

    if (mkdir("vault", 0700) != 0 && errno != EEXIST)
    {
        perror("Cannot create vault folder");
        return;
    }

    struct stat vault_info;

    if (lstat("vault", &vault_info) != 0 ||
        !S_ISDIR(vault_info.st_mode))
    {
        printf("Vault path is not a valid directory!\n");
        return;
    }

    sqlite3 *db;

    if (!open_vault_database(&db))
        return;

    char destination[1024];

    snprintf(destination, sizeof(destination),
             "vault/file_%ld_%d",
             (long)time(NULL), getpid());

    if (access(destination, F_OK) == 0)
    {
        printf("Destination already exists. Try again.\n");
        sqlite3_close(db);
        return;
    }

    if (rename(path, destination) != 0)
    {
        perror("Unable to move file");

        printf("The file may be on a different filesystem.\n");

        sqlite3_close(db);
        return;
    }

    sqlite3_stmt *statement;

    char *query =
        "INSERT INTO quarantine "
        "(original_path, vault_path) VALUES (?, ?);";

    int result = sqlite3_prepare_v2(
        db, query, -1, &statement, NULL);

    if (result == SQLITE_OK)
    {
        sqlite3_bind_text(
            statement, 1, path, -1, SQLITE_TRANSIENT);

        sqlite3_bind_text(
            statement, 2, destination, -1, SQLITE_TRANSIENT);

        result = sqlite3_step(statement);
    }

    sqlite3_finalize(statement);

    if (result != SQLITE_DONE)
    {
        printf("Database error. Restoring original file.\n");

        if (rename(destination, path) != 0)
            printf("WARNING: Manual recovery may be required.\n");

        sqlite3_close(db);
        return;
    }

    printf("\nFile quarantined successfully!\n");
    printf("Vault location: %s\n", destination);

    sqlite3_close(db);
}

void list_quarantined_files()
{
    sqlite3 *db;

    if (!open_vault_database(&db))
        return;

    sqlite3_stmt *statement;

    char *query =
        "SELECT id, original_path, quarantined_at "
        "FROM quarantine WHERE status='quarantined';";

    int result = sqlite3_prepare_v2(
        db, query, -1, &statement, NULL);

    if (result != SQLITE_OK)
    {
        printf("Unable to read quarantine records!\n");
        sqlite3_close(db);
        return;
    }

    printf("\n===== QUARANTINED FILES =====\n");

    while (sqlite3_step(statement) == SQLITE_ROW)
    {
        printf("\nID: %d\n",
               sqlite3_column_int(statement, 0));

        printf("Original Path: %s\n",
               sqlite3_column_text(statement, 1));

        printf("Date: %s\n",
               sqlite3_column_text(statement, 2));
    }

    printf("\n============================\n");

    sqlite3_finalize(statement);
    sqlite3_close(db);
}

void restore_file(int id)
{
    sqlite3 *db;

    if (!open_vault_database(&db))
        return;

    sqlite3_stmt *statement;

    char *query =
        "SELECT original_path, vault_path "
        "FROM quarantine "
        "WHERE id=? AND status='quarantined';";

    int result = sqlite3_prepare_v2(
        db, query, -1, &statement, NULL);

    if (result != SQLITE_OK)
    {
        printf("Database query failed!\n");
        sqlite3_close(db);
        return;
    }

    sqlite3_bind_int(statement, 1, id);

    result = sqlite3_step(statement);

    if (result != SQLITE_ROW)
    {
        printf("Quarantine record not found!\n");

        sqlite3_finalize(statement);
        sqlite3_close(db);
        return;
    }

    char original[1024];
    char stored[1024];

    snprintf(original, sizeof(original), "%s",
             sqlite3_column_text(statement, 0));

    snprintf(stored, sizeof(stored), "%s",
             sqlite3_column_text(statement, 1));

    sqlite3_finalize(statement);

    struct stat info;

    if (lstat(original, &info) == 0)
    {
        printf("Original location already exists!\n");
        printf("Restore cancelled to prevent overwriting.\n");

        sqlite3_close(db);
        return;
    }

    if (errno != ENOENT)
    {
        perror("Cannot check original location");
        sqlite3_close(db);
        return;
    }

    if (lstat(stored, &info) != 0 || !S_ISREG(info.st_mode))
    {
        printf("Quarantined file is missing or invalid!\n");
        sqlite3_close(db);
        return;
    }

    if (rename(stored, original) != 0)
    {
        perror("Unable to restore file");
        sqlite3_close(db);
        return;
    }

    char *update_query =
        "UPDATE quarantine SET status='restored' WHERE id=?;";

    result = sqlite3_prepare_v2(
        db, update_query, -1, &statement, NULL);

    if (result == SQLITE_OK)
    {
        sqlite3_bind_int(statement, 1, id);
        result = sqlite3_step(statement);
    }

    sqlite3_finalize(statement);

    if (result == SQLITE_DONE)
        printf("\nFile restored successfully!\n");
    else
        printf("\nFile restored, but database status update failed!\n");

    sqlite3_close(db);
}

void vault_menu()
{
    int choice;
    char input[1024];

    while (1)
    {
        printf("\n===== SAFESPACE VAULT =====\n");
        printf("1. Quarantine a file\n");
        printf("2. View quarantined files\n");
        printf("3. Restore a file\n");
        printf("0. Exit vault\n");

        printf("\nEnter your choice: ");

        if (fgets(input, sizeof(input), stdin) == NULL)
            return;

        choice = atoi(input);

        if (choice == 1)
        {
            printf("Enter complete file path: ");

            if (fgets(input, sizeof(input), stdin) == NULL)
                continue;

            input[strcspn(input, "\n")] = '\0';

            quarantine_file(input);
        }
        else if (choice == 2)
        {
            list_quarantined_files();
        }
        else if (choice == 3)
        {
            printf("Enter file ID to restore: ");

            if (fgets(input, sizeof(input), stdin) == NULL)
                continue;

            restore_file(atoi(input));
        }
        else if (choice == 0)
        {
            printf("Exiting vault...\n");
            break;
        }
        else
        {
            printf("Invalid choice!\n");
        }
    }
}
