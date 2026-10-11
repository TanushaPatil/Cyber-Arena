#include <stdio.h>
#include <stdlib.h>

void win()
{
    printf("\n=================================\n");
    printf("ACCESS GRANTED!\n");
    printf("FLAG: TECH{stack_attack}\n");
    printf("=================================\n");
}

void vulnerable()
{
    char buffer[64];

    printf("\nInput: ");
    fflush(stdout);

    gets(buffer);

    printf("\nYou entered: %s\n", buffer);
}

int main()
{
    printf("=================================\n");
    printf("          STACK ATTACK\n");
    printf("=================================\n");

    vulnerable();

    printf("\nNothing interesting happened.\n");

    return 0;
}