#ifndef HASHER_H
#define HASHER_H

#include <stdint.h>

typedef uint8_t uint8;

typedef struct { // Hash Result Object
    uint8 *piece_layer;
    uint8 *pieces_root;
    uint8 *hashv1;
} HASHHYBRID;

typedef struct { // Hash Result Object
    uint8 *piece_layer;
    uint8 *pieces_root;
} HASHV2;

typedef struct {
    uint8 *pieces;
} HASH;

HASHV2 *HasherV2(char *path, int piece_length);
HASHHYBRID *HasherHybrid(char *path, int piece_length);
HASH *Hasher(char **filelist, int piece_length);

#endif
