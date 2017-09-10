/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>
#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    //n cannot be non-positive integer
    if (n < 1)
    {
        return false;
    }
    //searching position
    int s_pos = n / 2;
    int left_bound = 0;
    int right_bound = n-1;
    //binary search with recursive function
    while (true)
    {
        if (value == values[s_pos])
        {
            return true;
        }
        
        else if ( value < values[s_pos])
        {
            right_bound = (s_pos - 1);
            s_pos = (right_bound - ((right_bound - left_bound) / 2));
        }
        else
        {
            left_bound = (s_pos + 1);
            s_pos = (left_bound + ((right_bound - left_bound) / 2));
        }
        //Worst case-scenario and exiting from while loop
        if (left_bound == right_bound)
        {
            if (value == values[s_pos])
            {
                return true;
            }
            else 
            {
                return false;
            }
        }
    }
    
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    //bubble sort
    int i;
    int j;
    int swap_counter = -1;
    while (swap_counter != 0)
    {
        //We should track greatest number every swap, because if the greatest number is at rightest in the list, it is not required to look anymore.
        int greatest = 0;
        //should initialize swap 0, because if numbers are not swapped, loop can be ended.
        swap_counter = 0;
        for (i = 0, j = 1; j < n; i++, j++)
        {
            //temp variable is for additional memory to swapping values[i] and values[j]
            int temp = 0;
            if (values[i] > values[j])
            {
                //get track greatest number
                if (values[i] > greatest)
                {
                    greatest = values[i];
                }
                //swap numbers
                temp = values[j];
                values[j] = values[i];
                values[i] = temp;
                swap_counter++;
            }
            
            if (values[j] > greatest)
            {
                greatest = values[j];
            }
        }
        //check whether greatest number is at the rightest in the list
        if (greatest == values[j])
        {
            // if greatest number at the rightest, we exclude that number
            n = n - 1;
        }
        
    }
}
