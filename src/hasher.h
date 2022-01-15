#ifndef HASHER_H
#define HASHER_H

#include <stdint.h>

typedef uint8_t uint8;

typedef struct { // Hash Result Object
    int count1;
    uint8 *hashv1;
    int count2;
    uint8 *piece_layer;
    uint8 *pieces_root;
} HASHHYBRID;

typedef struct { // Hash Result Object
    int count;
    uint8 *piece_layer;
    uint8 *pieces_root;
} HASHV2;

typedef struct {
    int count;
    uint8 *pieces;
} HASH;

void hexdigest(uint8 *hash);
HASHV2 *HasherV2(char *path, int piece_length);
HASHHYBRID *HasherHybrid(char *path, int piece_length);
HASH *Hasher(char **filelist, int piece_length);

#endif
