#include "safespace.h"
#include <sqlite3.h>

void save_storage_history(
    unsigned long long total,
    unsigned long long used,
    unsigned long long available,
    double percentage)
{
    sqlite3 *db;
    char *error = NULL;

    int result = sqlite3_open("database/safespace.db", &db);

    if (result != SQLITE_OK)
    {
        printf("Database connection failed!\n");
        sqlite3_close(db);
        return;
    }

    char *create_table =
        "CREATE TABLE IF NOT EXISTS storage_history ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "total_storage INTEGER,"
        "used_storage INTEGER,"
        "available_storage INTEGER,"
        "usage_percentage REAL,"
        "recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP"
        ");";

    result = sqlite3_exec(db, create_table, NULL, NULL, &error);

    if (result != SQLITE_OK)
    {
        printf("Table creation error: %s\n", error);
        sqlite3_free(error);
        sqlite3_close(db);
        return;
    }

    sqlite3_stmt *statement;

    char *insert_query =
        "INSERT INTO storage_history "
        "(total_storage, used_storage, available_storage, usage_percentage) "
        "VALUES (?, ?, ?, ?);";

    result = sqlite3_prepare_v2(db, insert_query, -1,
                                &statement, NULL);

    if (result == SQLITE_OK)
    {
        sqlite3_bind_int64(statement, 1, (sqlite3_int64)total);
        sqlite3_bind_int64(statement, 2, (sqlite3_int64)used);
        sqlite3_bind_int64(statement, 3, (sqlite3_int64)available);
        sqlite3_bind_double(statement, 4, percentage);

        sqlite3_step(statement);
    }

    sqlite3_finalize(statement);

    printf("\nStorage history saved successfully!\n");

    sqlite3_close(db);
}

void show_storage_history()
{
    sqlite3 *db;
    sqlite3_stmt *statement;

    int result = sqlite3_open("database/safespace.db", &db);

    if (result != SQLITE_OK)
    {
        printf("Cannot open storage database!\n");
        sqlite3_close(db);
        return;
    }

    char *query =
        "SELECT id, used_storage, usage_percentage, recorded_at "
        "FROM storage_history ORDER BY id DESC LIMIT 10;";

    result = sqlite3_prepare_v2(db, query, -1,
                                &statement, NULL);

    if (result != SQLITE_OK)
    {
        printf("Unable to read storage history!\n");
        sqlite3_close(db);
        return;
    }

    printf("\n===== STORAGE GROWTH HISTORY =====\n");

    while (sqlite3_step(statement) == SQLITE_ROW)
    {
        int id = sqlite3_column_int(statement, 0);

        sqlite3_int64 used =
            sqlite3_column_int64(statement, 1);

        double percentage =
            sqlite3_column_double(statement, 2);

        const unsigned char *date =
            sqlite3_column_text(statement, 3);

        printf("\nRecord ID: %d\n", id);

        printf("Used Storage: %.2f GB\n",
               used / (1024.0 * 1024 * 1024));

        printf("Usage: %.2f%%\n", percentage);

        printf("Date: %s\n", date);
    }

    printf("\n==================================\n");

    sqlite3_finalize(statement);
    sqlite3_close(db);
}
