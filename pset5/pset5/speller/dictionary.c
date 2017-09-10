/**
 * Implements a dictionary's functionality.
 */
#include <stdio.h>

#include <stdbool.h>

#include "dictionary.h"

#include <string.h>

#include <stdlib.h>

#include <ctype.h>

trie* root;
int word_count = 0;

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // Search words in tries data structure
    int location;
    trie* check_pointer = root;
    
    for (int i = 0; i < strlen(word); i++)
    {
        location = normalize(word[i]);
        if (check_pointer->children[location] == NULL)
        {
            return false;
        }
        //Existing node, jump it
        else
        {
            check_pointer = check_pointer->children[location];
        }
    }
    
    if (check_pointer->is_word == true)
    {
        return true;
    }
    else
    {
        return false;
    }
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // open dictionary file with reading mod
    FILE *dictionary_file = fopen(dictionary, "r");

    if (dictionary_file == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return 1;
    }
    
    root = malloc(sizeof(trie));
    
    if (root == NULL)
    {
        fclose(dictionary_file);
        return false;
    }
    
    for (int k = 0; k < 27; k++)
    {
        root->children[k] = NULL;
    }
    root->is_word = NULL;
    
    char word[LENGTH+1];
    
    
    while(fscanf(dictionary_file,"%s", word) != EOF)
    {
        int location;
        trie* traverse_pointer = root;        
        for (int i = 0; i < strlen(word); i++)
        {
            location = normalize(word[i]);
            
            //Non-exist node, allocate new node
            if (traverse_pointer->children[location] == NULL )
            {
                trie* node = malloc(sizeof(trie));
                
                if (node == NULL)
                {
                    fclose(dictionary_file);
                    return false;   
                } 
                node->is_word = NULL;
                for (int j = 0; j < 27; j++)
                {
                    node->children[j] = NULL;
                }

                traverse_pointer->children[location] = node;
                traverse_pointer = traverse_pointer->children[location];
            }
            //Existing node, jump it
            else
            {
                traverse_pointer = traverse_pointer->children[location];
            }
        }
        //set traverse->isword true
        traverse_pointer->is_word = true;
    }
    fclose(dictionary_file);
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    traverse(root);
    return word_count;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    recursive_unload(root);
    return true;
}

/**
 * Takes a letter, returns a value between 0-26 in alphabetical order
 * '\'' is 26th symbol.
 */
int normalize(char symbol)
{
    if (symbol != '\'' )
    {
        symbol = (tolower(symbol) - 97);
    }
    else
    {
        return 26;
    }
    
    return symbol;
}


/**
 * Estimate loaded dictionarie's size recursively.
 */
 
void traverse(trie *size_p)
{
    int i = 0;

    if (size_p->is_word == true)
    {
        word_count++;
    }
    
    for (i = 0; i < 27; i++)
    {
        if (size_p->children[i] != NULL)
        {
            traverse(size_p->children[i]);
        }
    }
}

/**
 * Unload loaded dictionary from memory recursively.
 */
void recursive_unload(trie* rec_pointer)
{
    int i = 0;
    
    for (i = 0; i < 27; i++)
    {
        if (rec_pointer->children[i] != NULL)
        {
            recursive_unload(rec_pointer->children[i]);
        }
    }
    free(rec_pointer);    
}