#ifndef SHA256_H
#define SHA256_H

#include <stdint.h>
#include <string.h>

#define SHA256_LENGTH 32
#define SHA256_CHUNK_LENGTH 64

typedef struct {
	uint8_t *hash;
	uint8_t chunk[SHA256_CHUNK_LENGTH];
	uint8_t *chunk_pos;
	size_t space_left;
	size_t total_len;
	uint32_t h[8];
} SHA256_CTX;

void SHA256(uint8_t hash[SHA256_LENGTH], const void *input, size_t len);
void SHA256Init(SHA256_CTX *context, uint8_t hash[SHA256_LENGTH]);
void SHA256Update(SHA256_CTX *context, const void *data, size_t len);
uint8_t *SHA256Final(SHA256_CTX *context);

#endif
