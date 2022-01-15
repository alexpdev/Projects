#include "src/hasher.c"

int main(int argc, char **argv)
{
    int piece_length = (int)pow(2.0, 14.0);
    printf("Hasher V1; Piece size %d; first path %s;\n\n", piece_length, argv[1]);
    HASH *hash;
    hash = Hasher(argv, piece_length);
    printf("Total size of pieces = %d", hash->count);
    hexdigest(hash->pieces);
    return 0;
}


// int main(int argc, char **argv)
// {
//     int piece_length = (int)pow(2.0, 14.0);
//     printf("Hasher V2; Piece size %d; path %s;\n\n", piece_length, argv[1]);
//     HASHV2* hash;
//     hash = HasherV2(argv[1], piece_length);
//     printf("Piece Layer: %d", hash->count);
//     hexdigest(hash->piece_layer);
//     printf("Pieces Root: 32");
//     hexdigest(hash->pieces_root);
//     return 0;
// }

// int main(int argc, char **argv){
//     int piece_length = (int)pow(2.0, 14.0);
//     printf("Hasher Hybrid; Piece size %d; path %s;\n\n", piece_length, argv[1]);
//     HASHHYBRID* hash;
//     hash = HasherHybrid(argv[1], piece_length);
//     printf("Piece Layer: %d", hash->count2);
//     hexdigest(hash->piece_layer);
//     printf("Pieces Root: 32");
//     hexdigest(hash->pieces_root);
//     printf("V1 Pieces: %d", hash->count1);
//     hexdigest(hash->hashv1);
//     return 0;
// }
