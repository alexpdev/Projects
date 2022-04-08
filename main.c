#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include "src/hasher.h"

#define V1SIZE 20
#define V2SIZE 32

int main1(int argc, char **argv)
{
    clock_t start, end;
    double timeused;
    start = clock();
    int piece_length = (int)pow(2.0, 14.0);
    // printf("Hasher V1; Piece size %d; first path %s;\n\n", piece_length, argv[1]);
    HASH *hash;
    hash = Hasher(argv, piece_length);
    printf("Total number of pieces = %d\n\n", hash->count);
    // fixedhexdigest(hash->pieces, hash->count * V1SIZE);
    end = clock();
    timeused = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time to execute = %f", timeused);
    return 0;
}


int main2(int argc, char **argv)
{
    clock_t start, end;
    double timeused;
    start = clock();
    int piece_length = (int)pow(2.0, 14.0);
    // printf("\n\nHasher V2; Piece size %d; path %s;\n\n", piece_length, argv[1]);
    HASHV2* hash;
    hash = HasherV2(argv[1], piece_length);
    // printf("\n\nPiece Layer: %d\n\n", hash->count);
    // fixedhexdigest(hash->piece_layer, V2SIZE * hash->count);
    // printf("\n\nPieces Root: 32\n\n");
    // fixedhexdigest(hash->pieces_root, V2SIZE);
    end = clock();
    timeused = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time to execute = %f", timeused);
    return 0;
}

int main3(int argc, char **argv)
{
    clock_t start, end;
    double timeused;
    start = clock();
    int piece_length = (int)pow(2.0, 14.0);
    // printf("\n\nHasher Hybrid; Piece size %d; path %s;\n\n", piece_length, argv[1]);
    HASHHYBRID* hash;
    hash = HasherHybrid(argv[1], piece_length);
    // printf("\n\nPiece Layer: %d\n\n", hash->count2);
    // fixedhexdigest(hash->piece_layer, V2SIZE * hash->count2);
    // printf("\n\nPieces Root: 32\n\n");
    // fixedhexdigest(hash->pieces_root, V2SIZE);
    // printf("\n\nV1 Pieces: %d\n\n", hash->count1);
    // fixedhexdigest(hash->hashv1, V1SIZE * hash->count1);
    end = clock();
    timeused = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time to execute = %f", timeused);
    return 0;
}


int main(int argc, char **argv)
{
    int r;
    r = main1(argc, argv);
    // r = main2(argc, argv);
    // r = main3(argc, argv);
    return 0;
}
