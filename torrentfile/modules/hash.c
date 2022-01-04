#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>
#include <sys/stat.h>
#include <inttypes.h>
#include "sha1.h"

void digest_to_hex(const unsigned char *digest, char *output)
{
    int i,j;
    char *c = output;

    for (i = 0; i < DIGEST_LENGTH/4; i++)
    {
        for (j = 0; j < 4; j++)
        {
            sprintf(c,"%02X", digest[i*4+j]);
            c += 2;
        }
        sprintf(c, " ");
        c += 1;
    }
    *(c - 1) = '\0';
}

int main(int argc, char **argv)
{
    char *filename = "temp.file";
    char *msg = "abc";
    FILE *fptr;
    fptr = fopen(filename, "rb");
    if (!fptr)
    {
        printf("ERROR!\n");
        exit(1);
    }
    struct stat sb;
    if (stat(filename, &sb) == -1){
        printf("ERROR\n");
        exit(1);
    }
    size_t total = sizeof msg * strlen(msg);
    SHA1_CTX context;
    SHA1Init(&context);
    unsigned char *digest = malloc(DIGEST_LENGTH);
    const unsigned char *data = (unsigned char *) msg;
    size_t len = strlen(msg);
    SHA1Update(&context, msg, len);
    unsigned char output[DIGEST_LENGTH];
    SHA1Final(digest, &context);
    printf("%s\n", digest);
    digest_to_hex(digest, output);
    printf("%s", output);
    return 0;
}
