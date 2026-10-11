#include <stdio.h>
#include <string.h>

void reveal_flag(void)
{
    const unsigned char data[] = {
        0x0E, 0x1F, 0x1D, 0x12, 0x21,
        0x28, 0x2E, 0x35, 0x38, 0x3B,
        0x39, 0x2F, 0x38, 0x39, 0x35,
        0x34, 0x1F, 0x38, 0x2E, 0x38,
        0x1F, 0x2B, 0x3E, 0x32, 0x39,
        0x35, 0x34, 0x2B, 0x30, 0x2C,
        0x39, 0x39, 0x35, 0x38, 0x2F,
        0x28, 0x2F, 0x2E, 0x2B, 0x2C
    };

    size_t i;

    printf("\nAccess granted.\n");
    printf("Flag: ");

    for (i = 0; i < sizeof(data); i++)
    {
        putchar(data[i] ^ 0x5A);
    }

    putchar('\n');
}

int check_key(const char *input)
{
    const unsigned char expected[] = {
        0x1B, 0x08, 0x0F, 0x1B, 0x18,
        0x0E, 0x1F, 0x17, 0x0E, 0x19,
        0x09, 0x08, 0x1B, 0x18
    };

    size_t length = strlen(input);
    size_t i;

    if (length != sizeof(expected))
    {
        return 0;
    }

    for (i = 0; i < sizeof(expected); i++)
    {
        if (((unsigned char)input[i] ^ 0x5A) != expected[i])
        {
            return 0;
        }
    }

    return 1;
}

int main(void)
{
    char license[128];

    printf("================================\n");
    printf("        BLACKBOX LICENSE\n");
    printf("================================\n\n");

    printf("Enter license key: ");

    if (fgets(license, sizeof(license), stdin) == NULL)
    {
        return 1;
    }

    license[strcspn(license, "\n")] = '\0';

    if (check_key(license))
    {
        reveal_flag();
    }
    else
    {
        printf("Invalid license key.\n");
    }

    return 0;
}