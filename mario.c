#include <stdio.h>
#include <cs50.h>
void oneline(int line);

int main(void)
{
    printf("Height: ");
    int height = get_int();
    while (height > 23 || height < 0 )
    {
        printf("Height: ");
        height = get_int();
    }
    for (int i = 1; i <= height; i++)
    {
        for (int j = 0; j < height - i; j++)
        {
        printf(" ");
        }    
        oneline(i);
        printf("  ");
        oneline(i);
        printf("\n");
    }
    
}

void oneline(int line)
{
    for (int i = 0; i < line; i++)
    {
        printf("#");
    }
}