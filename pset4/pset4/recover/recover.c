/**
 * Recovers deleted jpeg formatted images from a file.
 */
       
#include <stdio.h>
#include <stdlib.h>
FILE *img = NULL;

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }   
    
    // file name
    char *raw_file = argv[1];    
    
    // open input file 
    FILE *inptr = fopen(raw_file, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", raw_file);
        return 2;
    }
    
    unsigned char buffer[512];
    char filename[8];
    // for checking end of file. 
    int check_end = 1;
    int jpeg_count = 0;
    
    
    // as long as check_end is 1, it is not end of file
    while (check_end == 1)
    {
        check_end = fread(buffer, 512, 1, inptr);
    
        
        // start of jpeg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // we already found a jpeg
            if (jpeg_count != 0)
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", jpeg_count);
                img = fopen(filename, "w");
                fwrite(buffer, 512, 1, img);                
                jpeg_count++;
            }
            // our very first jpeg 
            else
            {
                sprintf(filename, "%03i.jpg", 0);
                img = fopen(filename, "w");
                fwrite(buffer, 512, 1, img);
                jpeg_count = 1;
            }
        }
        
        // not start of jpeg
        else
        {
            // bytes belongs to current jpeg file
            //also check whether it is end of file
            if (jpeg_count != 0 && check_end == 1)
            {
                fwrite(buffer, 512, 1, img);
            }
            // don't do anything because we don't encountered any jpegs, continue to iterate 
        }
        
    }

    // close remaning files due to file ending.
    fclose(img);
    fclose(inptr);
    
}