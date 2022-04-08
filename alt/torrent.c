#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include "sha.h"

#define HASHSIZE 20

struct HASH {
    long size;
    unsigned char *hash;
};

void HashExtend(struct HASH *hash, unsigned char *buffer, int size)
{
    for (int i = 0; i < size; i++)
    {
        hash->hash[hash->size] = buffer[i];
        hash->size += 1;
    }
}

void hexdigest(unsigned char *buffer, long size)
{
    printf("\n--- ");
    for (int i = 0; i < size; i++)
    {
        printf("%02X", buffer[i]);
    }
    printf(" ---\n");
}

struct HASH *Hasher(char *path, int piece_length)
{
    unsigned char *buffer = malloc(piece_length);
    struct HASH *hash = malloc(sizeof(struct HASH));
    FILE *fptr;
    fptr = fopen(path, "rb");
    fseek(fptr, 0, SEEK_END);
    long file_size = ftell(fptr);
    fseek(fptr, 0, SEEK_SET);
    printf("file size: %ld\n", file_size);
    int num_pieces = (int) floor(file_size / piece_length) + 1;
    long totalsize = num_pieces * HASHSIZE;
    unsigned char *hash_str = calloc(1, totalsize);
    unsigned char *hash_buff = malloc(HASHSIZE);
    int amount;
    int counter = 0;
    hash->hash = hash_str;
    hash->size = 0;
    while (1)
    {
        printf(" %d ", counter);
        counter += 1;
        amount = fread(buffer, 1, piece_length, fptr);
        if (amount < piece_length)
        {
            if (!amount){break;}
            SHA1(hash_buff, buffer, amount);
            HashExtend(hash, hash_buff, HASHSIZE);
            break;
        }
        SHA1(hash_buff, buffer, amount);
        HashExtend(hash, hash_buff, HASHSIZE);
    }
    fclose(fptr);
    printf("complete %d", counter);
    return hash;
}


int main(int argc, char **argv)
{
    clock_t start, end;
    double timeused;
    start = clock();
    char *path = argv[1];
    int piece_length = pow(2,20);
    struct HASH *hash;
    printf("\n%s  - %d\n", path, piece_length);
    hash = Hasher(path, piece_length);
    end = clock();
    timeused = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time to execute = %f", timeused);
    return 0;
}
