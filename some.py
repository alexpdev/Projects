from torrentfile.hasher import Hasher, HasherV2, HasherHybrid
import os
import time

def timerun():
    path = "testfile"
    piece_length = 2**14
    hasher = HasherV2
    then = time.time()
    if hasher == Hasher:
        b = []
        a = hasher(path, piece_length)
        for i in a:
            b.append(i)
        c = b''.join(b)
        print(len(b))
    else:
        a = hasher(path, piece_length)
        print(len(a.layer_hashes))
    print(time.time() - then)

if __name__ == '__main__':
    timerun()
