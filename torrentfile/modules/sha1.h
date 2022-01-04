#ifndef SHA1_H
#define SHA1_H
#include "stdint.h"

typedef struct
{
    uint32_t state[5];
    uint32_t count[2];
    unsigned char buffer[64];
} SHA1_CTX;

#define SHA1_LENGTH 20

void SHA1(char *hash_out, const char *str, int len);
void SHA1Init(SHA1_CTX * context);
void SHA1Update(SHA1_CTX * context, const unsigned char *data, uint32_t len);
void SHA1Final(unsigned char digest[SHA1_LENGTH], SHA1_CTX * context);

#endif
