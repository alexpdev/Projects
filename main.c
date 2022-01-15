#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "src/hasher.h"

#define V1SIZE 20
#define V2SIZE 32

// int main(int argc, char **argv)
// {
//     int piece_length = (int)pow(2.0, 14.0);
//     printf("Hasher V1; Piece size %d; first path %s;\n\n", piece_length, argv[1]);
//     HASH *hash;
//     hash = Hasher(argv, piece_length);
//     printf("Total number of pieces = %d\n\n", hash->count);
//     fixedhexdigest(hash->pieces, hash->count * V1SIZE);
//     return 0;
// }


// int main(int argc, char **argv)
// {
//     int piece_length = (int)pow(2.0, 14.0);
//     printf("\n\nHasher V2; Piece size %d; path %s;\n\n", piece_length, argv[1]);
//     HASHV2* hash;
//     hash = HasherV2(argv[1], piece_length);
//     printf("\n\nPiece Layer: %d\n\n", hash->count);
//     fixedhexdigest(hash->piece_layer, V2SIZE * hash->count);
//     printf("\n\nPieces Root: 32\n\n");
//     fixedhexdigest(hash->pieces_root, V2SIZE);
//     return 0;
// }

int main(int argc, char **argv){
    int piece_length = (int)pow(2.0, 14.0);
    printf("\n\nHasher Hybrid; Piece size %d; path %s;\n\n", piece_length, argv[1]);
    HASHHYBRID* hash;
    hash = HasherHybrid(argv[1], piece_length);
    printf("\n\nPiece Layer: %d\n\n", hash->count2);
    fixedhexdigest(hash->piece_layer, V2SIZE * hash->count2);
    printf("\n\nPieces Root: 32\n\n");
    fixedhexdigest(hash->pieces_root, V2SIZE);
    printf("\n\nV1 Pieces: %d\n\n", hash->count1);
    fixedhexdigest(hash->hashv1, V1SIZE * hash->count1);
    return 0;
}
