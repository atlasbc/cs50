#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
bool check_keyword(string key);
void make_mod(string key);

int main(int argc, string argv[])
{
    string keyword = argv[1];
    //checking whether command line has only single argument and contains alphabetical letters
    if (argc != 2 || !check_keyword(keyword))
    {
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    int n = strlen(keyword);
    make_mod(keyword);
    //this is plain_text
    printf("plaintext: ");
    string p = get_string(); 
    if (p != NULL)
    {
        int m = strlen(p);
        int j = 0;
        printf("ciphertext: ");
        for (int i = 0; i < m; i++)
        {
            //if keyword's letter alphabetical cipher plaintext's letter with keyword's letter
            if isalpha(p[i])
            {
                //small letters should begin 'a' after 'z'
                if (keyword[j] + p[i] > 122)
                {
                    printf("%c", (keyword[j]+p[i] - 26));
                }
                //big letters should begin 'A' after 'Z'
                else if (keyword[j]+p[i] > 90 && p[i] < 90 )
                {
                    printf("%c", (keyword[j] + p[i] - 26));
                }
                else
                {
                    printf("%c", (keyword[j]+ p[i]));
                }
                j = (j+1) % n;
            }
            //if keyword's letter non-alphabetical print plaintext's letter without changing
            else
            {
                printf("%c", p[i]);
            }
        }
        printf("\n");
        return 0;
    }
}
//This Function checks key whether it contains non-alphabetic symbols
bool check_keyword(string key)
{
    int n = strlen(key);
    for (int i = 0; i < n; i++)
    {
        if (isalpha(key[i]) == false)
        {
            return false;
        }
        
    }
    return true;
}
//This function makes keyword's letter modulo(26)
void make_mod(string key)
{
    int n = strlen(key);
    for (int i= 0;  i < n; i++)
    {
        if (isupper(key[i]))
        {
            key[i] = key[i] % 65;
        }
        else
        {
            key[i] = key[i] % 97;
        }
    }
}