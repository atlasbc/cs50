#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    //command line should take 1 argument
    if (argc != 2)
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }
    // we should convert string to int
    int k = atoi(argv[1]);
    //command line should take non-negative integer
    if (k < 1)
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }
    
    else
    {
        printf("plaintext: ");
        string p = get_string();
        if (p != NULL)
        {
            printf("ciphertext: ");
            for (int i = 0, n = strlen(p); i < n; i++)
            {
                //if plaintexts' letter is alphabetical do cipher
                if isalpha(p[i])
                {
                    //small letters should begin 'a' after 'z'
                    if ((k%26) + p[i] > 122)
                    {
                        printf("%c", ((k%26) + p[i] - 26));
                    }
                    //big letters should begin 'A' after 'Z'
                    else if ((k%26)+p[i] > 90 && p[i] < 90 )
                    {
                        printf("%c", (k%26 + p[i] - 26));
                    }
                    else
                    {
                        printf("%c", ((k%26)+ p[i]));    
                    }
                }
                //if plaintext is non-alphabetical jump without ciphering
                else
                {
                    printf("%c", p[i]);
                }
            }
            printf("\n");
            return 0;
        }    
    }
    
}