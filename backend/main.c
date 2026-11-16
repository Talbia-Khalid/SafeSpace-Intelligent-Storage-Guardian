#include <stdio.h>
#include "safespace.h"

int main()
{
    printf("================================\n");
    printf("       Welcome to SafeSpace\n");
    printf("================================\n");

    printf("\nChecking system storage...\n");

    check_storage();

    analyze_directory();

    printf("\nSafeSpace analysis completed!\n");

    return 0;
}
