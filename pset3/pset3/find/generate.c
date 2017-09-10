/**
 * generate.c
 *
 * Generates pseudorandom numbers in [0,MAX), one per line.
 *
 * Usage: generate n [s]
 *
 * where n is number of pseudorandom numbers to print
 * and s is an optional seed
 */
 
#define _XOPEN_SOURCE

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// upper limit on range of integers that can be generated
#define LIMIT 65536

int main(int argc, string argv[])
{
    // Command line must take 1 or 2 argument
    if (argc != 2 && argc != 3)
    {
        printf("Usage: ./generate n [s]\n");
        return 1;
    }

    // convert entered number from string to int
    int n = atoi(argv[1]);

    // if command line takes 2 argument, this means a seed number is entered. This seed number changes random numbers according to linear congruential formula.
    // else seed number takes the system's time as numbers
    if (argc == 3)
    {
        srand48((long) atoi(argv[2]));
    }
    else
    {
        srand48((long) time(NULL));
    }
    
    // n is entered numbers that must be generated.
    //drand generates random float numbers with uniform distribution in interval [0.0, 1.0]
    //for loop generates n amount of random numbers. Also it converts floating numbers to int.
    for (int i = 0; i < n; i++)
    {
        printf("%i\n", (int) (drand48() * LIMIT));
    }

    // success
    return 0;
}
