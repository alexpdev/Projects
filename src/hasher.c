#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <sys/stat.h>
#include <math.h>
#include <stdbool.h>
#include "sha1.h"
#include "sha256.h"

#define BLOCK_SIZE 16384

void showhash(uint8_t *hash, size_t len)
{
    int i;
    printf("\n");
    if (!len)
    {
        for (i = 0; hash[i] != (uint8_t)'\0'; i++)
            printf("%02X", (unsigned char)hash[i]);
    } else {
        for (i = 0; i < len; i++)
            printf("%02X", (unsigned char)hash[i]);
    }
    printf("\n");
}

uint8_t *concat(uint8_t *hash, uint8_t *out_hash, size_t len)
{
    uint8_t *new_hash = (uint8_t *)malloc(len + 20 + 1);
    printf("\n");
    if (hash) {
        for (int i = 0; i < len; i++){
            new_hash[i] = hash[i];
            printf("%02X", (unsigned char)hash[i]);
        }
    } else {hash = (uint8_t *)malloc(20);}
    for (int j = len; j < len + 20; j++){
        new_hash[j] = out_hash[j];
        printf("%02X", (unsigned char)out_hash[j]);
    }
    new_hash[len+20] = (uint8_t)'\0';
    printf("\n");
    return new_hash;
}

void fillbuff(uint8_t *buffer, uint8_t *subbuf, int buflen, int sublen)
{
    for (int i = buflen; i < buflen+sublen; i++)
        buffer[i] = subbuf[i - buflen];
}


uint8_t *sha1hashfiles(char **filelist, int qty, int piece_length){
    int i, amount, remLength, sub_length;
    char *path;
    FILE *fptr;
    uint8_t *subbuff;
    uint8_t *hash = NULL;
    uint8_t *out_hash = (uint8_t *)malloc(20);
    uint8_t *buffer = (uint8_t *)malloc(piece_length);
    size_t hashLength = 0;
    bool remset = false;
    for (i = 1; i < qty + 1; i++)
    {
        path = filelist[i];
        printf("# %d Filename: %s\n", i, path);
        fptr = fopen(path, "rb");
        while (true)
        {
            if (remset)
            {
                sub_length = piece_length - remLength;
                subbuff = (uint8_t *)malloc(sub_length);
                int sub_amount = fread(subbuff, 1, sub_length, fptr);
                fillbuff(buffer, subbuff, remLength, sub_amount);
                amount = remLength + sub_amount;
                remset = false;
            }
            else
            {
                amount = fread(buffer, i, piece_length, fptr);
            }
            if (amount < piece_length)
            {
                fclose(fptr);
                if (amount)
                {
                    remLength = amount;
                    remset = true;
                }
                break;
            }
            remset = false;
            SHA1(out_hash, buffer, amount);
            hash = concat(hash, out_hash, hashLength);
            hashLength += 20;
            printf("%s\n", (char *)hash);
        }
    }
    if (remset)
    {
        SHA1(out_hash, buffer, amount);
        hash = concat(hash, out_hash, hashLength);
        hashLength += 20;
    }
    return hash;
}

int main(int argc, char *argv[])
{
    // uint8_t *hash;
    int piece_length = BLOCK_SIZE;
    sha1hashfiles(argv, 1, piece_length);
    return 0;
}
