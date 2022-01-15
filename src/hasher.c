#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <math.h>
#include "sha.h"
#include "hasher.h"

#define BLOCKSIZE 16384
#define HASHSIZE 32
#define V1HASHSIZE 20


typedef uint8_t uint8;


typedef struct Node {  // Linked List Node Item
    uint8 *hash;
    struct Node *next;
} Node;


typedef struct {  // Linked List of layer hashes
    Node *start;
    Node *end;
    int count;
} Layer;


Layer *newLayer()
{
    // Creates a new linked list
    Layer *layer = (Layer *)malloc(sizeof(Layer));
    layer->start = NULL;
    layer->end = NULL;
    layer->count = 0;
    return layer;
}


void fixedhexdigest(uint8 *hash, int len)
{
    for (int i = 0; i < len; i++)
    {
        printf("%02X", hash[i]);
    }
}

void hexdigest(uint8 *hash)
{
    for (int i = 0; (char) hash[i] != '\0'; i++)
    {
        printf("%02X", hash[i]);
    }
}


void showTree(Layer *layer)
{
    printf("\n\n");
    Node *current = layer->start;
    while (current != NULL)
    {
        printf("----  ");
        hexdigest(current->hash);
        printf("  ----\n");
        current = current->next;
    }
    printf("\n\n");
}


uint8 *hashJoin(uint8 *hash1, uint8 *hash2)
{
    uint8 *joined = (uint8 *)malloc(HASHSIZE * 2);
    for (int i = 0; i < HASHSIZE; i++){
        joined[i] = hash1[i];
    }
    for (int j = 0; j < HASHSIZE; j++){
        joined[HASHSIZE+j] = hash2[j];
    }
    uint8 *hash3 = (uint8 *)malloc(HASHSIZE);
    SHA256(hash3, joined, HASHSIZE*2);
    return hash3;
}


void deleteLayer(Layer *layer)
{
    Node *start = layer->start;
    while (start)
    {
        Node *next = start->next;
        free(start->hash);
        free(start);
        start = next;
    }
    free(layer);
}


void addNode(Layer *layer, uint8 *hash)
{
    Node *newnode = (Node *)malloc(sizeof(Node));
    newnode->hash = hash;
    newnode->next = NULL;
    if (layer->start)
    {
        Node *end = layer->end;
        end->next = newnode;
        layer->end = newnode;
    }
    else
    {
        layer->start = newnode;
        layer->end = newnode;
    }
    layer->count = layer->count + 1;
}


void fill_hash(uint8 *seq, Layer *layer, int size)
{
    int index = 0;
    Node *current = layer->start;
    while (current != NULL)
    {
        for (int i = 0; i < size; i++)
        {
            seq[index] = current->hash[i];
            index += 1;
        }
        current = current->next;
    }
}


HASH *Hasher(char **filelist, int piece_length)
{
    Layer *layer = newLayer();
    int amount;
    FILE *fptr;
    uint8 *partial = NULL;
    uint8 *buffer = (uint8 *)malloc(piece_length);
    uint8 *output;
    int residue = 0;
    for (int i = 1; filelist[i] != NULL; i++)
    {
        fptr = fopen(filelist[i], "rb");
        while (true)
        {
            if (!partial)
            {
                amount = fread(buffer, 1, piece_length, fptr);
            }
            else
            {
                int subsize = piece_length - residue;
                uint8 *subbuff = (uint8 *)malloc(subsize);
                int amount = fread(subbuff, 1, subsize, fptr);
                for (int j = 0; j < amount; j++)
                {
                    buffer[residue + j] = subbuff[j];
                }
            }
            if (amount < piece_length)
            {
                fclose(fptr);
                if (!amount) break;
                partial = buffer;
                residue = amount;
                break;
            }
            output = (uint8 *)malloc(V1HASHSIZE);
            SHA1(output, buffer, piece_length);
            addNode(layer, output);
            partial = NULL;
        }
    }
    if (partial)
    {
        output = (uint8 *)malloc(V1HASHSIZE);
        SHA1(output, buffer, amount);
        addNode(layer, output);
    }
    // showTree(layer);
    uint8 *pieces = (uint8 *)malloc(V1HASHSIZE * layer->count);
    fill_hash(pieces, layer, V1HASHSIZE);
    HASH *hash = (HASH *)malloc(sizeof(HASH));
    hash->pieces = pieces;
    hash->count = layer->count;
    return hash;
}


uint8 *get_padding()
{
    uint8 *padding = (uint8 *)malloc(HASHSIZE);
    for (int i = 0; i < HASHSIZE; i++)
    {
        padding[i] = 0;
    }
    return padding;
}


uint8 *merkle_root(Layer *layer)
{
    int count = layer->count;
    while (count > 1)
    {
        Node *current = layer->start;
        Node *next = current->next;
        Node *last = current;
        int index = 0;
        while (true)
        {
            uint8 *partial = hashJoin(current->hash, next->hash);
            last->hash = partial;
            index++;
            current = next->next;
            if (!current) break;
            next = current->next;
            last = last->next;
        }
        count = index;
        layer->end = last;
        last->next = NULL;
    }
    return layer->start->hash;
}


uint8 *get_pad_piece(int n)
{
    uint8 *padding;
    Layer *layer = newLayer();
    for (int i = 0; i < n; i++)
    {
        padding = get_padding();
        addNode(layer, padding);
    }
    return merkle_root(layer);
}




HASHV2 *HasherV2(char *path, int piece_length)
{
    int amount, next_pow2, total, remaining, blocks_per_piece;
    // printf("243\n");
    Layer *layer;
    Layer *layer_hashes = newLayer();
    FILE *fptr = fopen(path, "rb");
    uint8 *buffer = (uint8 *)malloc(BLOCKSIZE);
    total = 0;
    blocks_per_piece = (int) floor(piece_length / BLOCKSIZE);
    // printf("250\n");
    while (true)
    {
        layer = newLayer();
        uint8 *piece;
        // printf("255\n");
        for (int i = 0; i < blocks_per_piece; i++)
        {
            amount = fread(buffer, 1, BLOCKSIZE, fptr);
            total += amount;
            if (!amount) break;
            uint8 *hash = (uint8 *)malloc(amount);
            SHA256(hash, buffer, amount);
            addNode(layer, hash);
        }
        if (!layer->count) break;
        if (layer->count < blocks_per_piece)
        {
            if (!layer_hashes->count)
            {
                next_pow2 = 1 << (int) floor((log(total)/log(2)) + 1);
                remaining = (int) ((next_pow2 - total) / BLOCKSIZE) + 1;
            }
            else
            {
                remaining = blocks_per_piece - layer->count;
            }
            uint8 *padding;
            for (int j = 0; j < remaining; j++)
            {
                padding = get_padding();
                addNode(layer, padding);
            }
        }
        // printf("284\n");
        piece = merkle_root(layer);
        addNode(layer_hashes, piece);
        // printf("287\n");
    }
    // showTree(layer_hashes);
    int n = layer_hashes->count;
    uint8 *piece_layer = (uint8 *)malloc(HASHSIZE * n);
    fill_hash(piece_layer, layer_hashes, HASHSIZE);
    // printf("293\n");
    if (!(n && ((n & (-n))== n)))
    {
        next_pow2 = 1 << (int) floor((log(n)/log(2)) + 1);
        remaining = next_pow2 - n;
        uint8 *piece;
        for (int k = 0; k < remaining; k++)
        {
            piece = get_pad_piece(blocks_per_piece);
            addNode(layer_hashes, piece);
        }
    }
    uint8 *roothash;
    // printf("306\n");
    roothash = merkle_root(layer_hashes);
    // hexdigest(roothash);
    HASHV2 *result = (HASHV2 *)malloc(sizeof(HASHV2));
    result->piece_layer = piece_layer;
    result->count = n;
    result->pieces_root = roothash;
    fclose(fptr);
    // printf("313\n");
    return result;
}


HASHHYBRID *HasherHybrid(char *path, int piece_length)
{
    int amount, next_pow2, total, remaining, blocks_per_piece;
    total = 0;
    bool final = false;
    Layer *layer;
    Layer *layer_hashes = newLayer();
    Layer *layerV1 = newLayer();
    uint8 *bufferV1 = (uint8 *)malloc(piece_length);
    FILE *fptr = fopen(path, "rb");
    uint8 *buffer = (uint8 *)malloc(BLOCKSIZE);
    blocks_per_piece = (int) floor(piece_length / BLOCKSIZE);
    while (true)
    {
        int buffer_pos = 0;
        layer = newLayer();
        for (int i = 0; i < blocks_per_piece; i++)
        {
            amount = fread(buffer, 1, BLOCKSIZE, fptr);
            total += amount;
            if (!amount) break;
            uint8 *hash = (uint8 *)malloc(amount);
            SHA256(hash, buffer, amount);
            addNode(layer, hash);
            for (int j = 0; j < amount; j++)
            {
                bufferV1[buffer_pos] = buffer[j];
                buffer_pos += 1;
            }
        }
        if (!layer->count) break;
        if (layer->count < blocks_per_piece)
        {
            final = true;
            if (!layer_hashes->count)
            {
                next_pow2 = 1 << (int) floor((log(total)/log(2)) + 1);
                remaining = (int) ((next_pow2 - total) / BLOCKSIZE) + 1;
            }
            else
            {
                remaining = blocks_per_piece - layer->count;
            }
            uint8 *padding;
            for (int k = 0; k < remaining; k++)
            {
                padding = get_padding();
                addNode(layer, padding);
            }
        }
        uint8 *piece;
        uint8 *hashV1 = (uint8 *)malloc(V1HASHSIZE);
        if (final)
        {
            int remains = piece_length - buffer_pos
            for (int t = 0; t < remains; t++)
            {
                bufferv1[buffer_pos] = NULL;
                buffer_pos += 1
            }
        }
        SHA1(hashV1, bufferV1, buffer_pos);
        piece = merkle_root(layer);
        addNode(layer_hashes, piece);
        addNode(layerV1, hashV1);
    }
    // showTree(layer_hashes);
    int n2 = layer_hashes->count;
    int n1 = layerV1->count;
    uint8 *piece_layer = (uint8 *)malloc(HASHSIZE * n2);
    uint8 *v1pieces = (uint8 *)malloc(V1HASHSIZE * n1);
    fill_hash(piece_layer, layer_hashes, HASHSIZE);
    fill_hash(v1pieces, layerV1, V1HASHSIZE);
    if (!(n2 && ((n2 & (-n2))== n2)))
    {
        next_pow2 =  1 << (int)floor((log(n2)/log(2)) + 1);
        remaining = next_pow2 - n2;
        uint8 *piece;
        for (int l = 0; l < remaining; l++){
            piece = get_pad_piece(blocks_per_piece);
            addNode(layer_hashes, piece);
        }
    }
    uint8 *roothash;
    roothash = merkle_root(layer_hashes);
    HASHHYBRID *result = (HASHHYBRID *)malloc(sizeof(HASHHYBRID));
    result->piece_layer = piece_layer;
    result->count2 = n2;
    result->pieces_root = roothash;
    result->count1 = n1;
    result->hashv1 = v1pieces;
    fclose(fptr);
    return result;
}


// int main(int argc, char **argv)
// {
//     int piece_length = (int)pow(2.0, 16.0);
//     printf("\npiece length = %d\n", piece_length);
//     printf("%s\n", argv[1]);
//     HASH *hash;
//     hash = Hasher(argv, piece_length);
//     hexdigest(hash->pieces);
//     HASHV2* resultv2;
//     resultv2 = HasherV2(argv[1], piece_length);
//     hexdigest(resultv2->piece_layer);
//     hexdigest(resultv2->pieces_root);
//     HASHHYBRID* resulthybrid;
//     resulthybrid = HasherHybrid(argv[1], piece_length);
//     hexdigest(resulthybrid->piece_layer);
//     hexdigest(resulthybrid->pieces_root);
//     hexdigest(resulthybrid->hashv1);
//     return 0;
// }
