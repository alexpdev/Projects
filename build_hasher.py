from cffi import FFI

ffi = FFI()
HEADER = """
typedef uint8_t uint8;

typedef struct {
    uint8 *piece_layer;
    uint8 *pieces_root;
    uint8 *hashv1;
} HASHHYBRID;

typedef struct {
    uint8 *piece_layer;
    uint8 *pieces_root;
} HASHV2;

typedef struct {
    uint8 *pieces;
} HASH;
HASHV2 *HasherV2(char *path, int piece_length);
HASHHYBRID *HasherHybrid(char *path, int piece_length);
HASH *Hasher(char **filelist, int piece_length);
"""

ffi.cdef(HEADER)
ffi.set_source(
    "_hasher",
    """
    #include "hasher.h"
    #include "sha.h"
    """,
    sources=['src/hasher.c', 'src/sha.c'],
)

if __name__ == "__main__":
    ffi.compile(verbose=True)
