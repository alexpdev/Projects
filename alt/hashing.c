#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "sha.h"


#define HASHSIZE 20

unsigned char *hash_file(char *path)
{
    FILE *fptr = fopen(path, "rb");
    fpos_t start, end;
    fgetpos(fptr, &start);
    fseek(fptr, 0, SEEK_END);
    fgetpos(fptr, &end);
    fsetpos(fptr, &start);
    printf("%lld", end);
    unsigned char *buffer = malloc(end);
    fread(buffer, 1, (size_t)end, fptr);
    unsigned char *hash = malloc(HASHSIZE);
    SHA1(hash, buffer, (size_t)end);
    fclose(fptr);
    return hash;
}


int power(int base, int exponent)
{
    int value = base;
    for (int i=0; i<exponent; i++)
        value = value * base;
    return value;
}

void hexdigest(unsigned char *seq, size_t len)
{
    printf("\n----- ");
    for (size_t i=0;i<len;i++)
    {
        printf("%02X", seq[i]);
    }
    printf(" -----\n");
}

int main(int argc, char **argv)
{
    char *path = argv[1];
    clock_t start, end;
    double time_used;
    start = clock();
    unsigned char *hash;
    hash = hash_file(path);
    end = clock();
    time_used = (double) end - start;
    printf("\n%f\n", time_used);
    hexdigest(hash, HASHSIZE);
}
