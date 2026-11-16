#include <stdio.h>
#include "safespace.h"

int main()
{
    printf("================================\n");
    printf("       Welcome to SafeSpace\n");
    printf("================================\n");

    printf("\nChecking system storage...\n");

    check_storage();

    return 0;
}
