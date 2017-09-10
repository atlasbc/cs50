#include <stdio.h>
#include <cs50.h>

int main(void)
{
    printf("Minute: ");
    int minute = get_int();
    int bottle = 12*minute;
    printf("Bottle: %i\n", bottle);
}
