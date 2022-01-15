from _hasher import lib, ffi

print(vars(lib))

piece_length = 2**15
path = ffi.new("char[]", b"testfile")
print(path)
output = lib.HasherV2(path, piece_length)
print(output)
pieces_root = ffi.unpack(output.pieces_root, )
layer_hashes = ffi.unpack(output.piece_layer)
print(pieces_root)
print(layer_hashes)
