#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>


int main(void)
{
    //ask for a name
    string name = get_string();
    int name_length = strlen(name);
    
    for (int i = 0; i < name_length; i++ )
    {
        //checking whether 2 spaces are consecutive and to be sure we are not out of the array(avoiding segmentation fault)
        if (name[i] == ' ' && name[i+1] != ' ' && (i + 1) < name_length)
        {
            printf("%c", toupper(name[i+1]));
        }
        //checking whether the first letter is a letter
        else if ( i == 0 && name[i] != ' ')
        {
            printf("%c", toupper(name[i]));
        }
    }
    printf("\n");
}