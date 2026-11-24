#include <stdio.h>
#include <string.h>
#include "safespace.h"

int main(int argc, char *argv[])
{
    char path[1024];

    // GUI integration mode: Storage Analyzer
    if (argc > 1 && strcmp(argv[1], "--storage") == 0)
    {
        check_storage();
        return 0;
    }

    // GUI integration mode: Folder Analyzer
    if (argc > 2 && strcmp(argv[1], "--folder") == 0)
    {
        analyze_directory(argv[2]);
        return 0;
    }

    // GUI integration mode: Duplicate Detector
    if (argc > 2 && strcmp(argv[1], "--duplicates") == 0)
    {
      detect_duplicates(argv[2]);
      return 0;
    }

    // GUI integration mode: Activity Monitor
     if (argc > 2 && strcmp(argv[1], "--monitor") == 0)
    {
       monitor_directory(argv[2]);
       return 0;
    }

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
    generate_storage_report(path);
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
