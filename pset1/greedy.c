#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    int total = 0;
    printf("O hai! How much change is owed?\n");
    float debt = get_float();
    while (debt < 0)
    {
        printf("How much change is owed?\n");
        debt = get_float();
    }
    int cent = round(debt*100);
    while (cent > 0)
    {
        if (cent >= 25)
        {
            cent = cent - 25;
            total++;
        }
        else if (cent >= 10)
        {
            cent = cent - 10;
            total++;
        }
        else if (cent >= 5)
        {
            cent = cent - 5;
            total++;
        }
        else
        {
            cent = cent - 1;
            total++;
        }
    }
    printf("%i\n", total);
}
