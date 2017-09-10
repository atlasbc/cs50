/**
 * Declares a dictionary's functionality.
 */

#ifndef DICTIONARY_H
#define DICTIONARY_H

#include <stdbool.h>

// maximum length for a word
// (e.g., pneumonoultramicroscopicsilicovolcanoconiosis)
#define LENGTH 45

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word);

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary);

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void);

/**
 * Unloads dictionary from memory.  Returns true if successful else false.
 */
bool unload(void);

/**
 * Takes a letter, returns a value between 0-26 in alphabetical order
 * '\'' is 26th symbol.
 */
int normalize(char symbol);

typedef struct trie
{
    bool is_word;
    struct trie *children[27];
}
trie;

/**
 * Estimate loaded dictionaries size recursively.
 */
void traverse(trie *size_p);

/**
 * Unload loaded dictionary from memory recursively.
 */
void recursive_unload(trie* rec_pointer);

#endif // DICTIONARY_H
