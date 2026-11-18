#include <stdio.h>
#include <string.h>
#include "safespace.h"

int main()
{
    char path[1024];

    printf("================================\n");
    printf("       Welcome to SafeSpace\n");
    printf("================================\n");

    printf("\nChecking system storage...\n");

    check_storage();
    show_storage_history();

    printf("\nEnter folder path to analyze: ");

    if (fgets(path, sizeof(path), stdin) == NULL)
    {
        printf("Invalid input!\n");
        return 1;
    }

    path[strcspn(path, "\n")] = '\0';

    analyze_directory(path);

    detect_duplicates(path);
    cleanup_recommendations(path);
    emergency_mode(path);
    storage_health_score();
    vault_menu();

    char choice;

printf("\nDo you want to start file activity monitoring? (y/n): ");
scanf(" %c", &choice);

if (choice == 'y' || choice == 'Y')
{
    monitor_directory(path);
}

    printf("\nSafeSpace analysis completed!\n");

    return 0;
}
