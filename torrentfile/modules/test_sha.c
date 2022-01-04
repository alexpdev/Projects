#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>
#include <sys/stat.h>
#include <inttypes.h>
#include "sha1.h"
#include "sha256.h"

#ifndef SHA256_H
#define SHA256_LENGTH 32
#define SHA256_CHUNK_LENGTH 64
#endif
#ifndef SHA1_H
#define SHA1_LENGTH 20
#endif
char *sha1abc = "a9993e364706816aba3e25717850c26c9cd0d89d";
char *sha256abc = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad";

void digest_to_hex(const uint8_t *digest, char *output, int len)
{
    int i,j;
    char *c = output;

    for (i = 0; i < len/4; i++)
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



void test(){
    printf("test2\n");
    printf("Message: abc\n");
    uint8_t *msg = (uint8_t *)"abc";
    uint8_t *sha1_digest = malloc(20);
    SHA1(sha1_digest, msg, strlen((char *)msg));
    char *out = malloc(20);
    digest_to_hex(sha1_digest, out, 20);
    printf("%s\n",out);

}

int main(int argc, char **argv)
{
    printf("starting\n");
    uint8_t *msg = (uint8_t *)"abc";
    uint8_t *sha1_digest = malloc(20);
    uint8_t *sha256_digest = malloc(SHA256_LENGTH);
    size_t len = strlen((char *)msg);
    SHA1(sha1_digest, msg, len);
    SHA256(sha256_digest, msg, len);
    char *sha1output = malloc(20);
    char *sha256output = malloc(SHA256_LENGTH);
    digest_to_hex(sha1_digest, sha1output, 20);
    digest_to_hex(sha256_digest, sha256output, SHA256_LENGTH);
    printf("sha1 = %s\n", sha1output);
    printf("sha256 = %s\n", sha256output);
    test();
    return 0;
}
