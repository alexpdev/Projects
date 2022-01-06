from cffi import FFI

CDEF = '''

'''

ffibuilder = FFI()
ffibuilder.cdef(CDEF)
ffibuilder.set_source('_shacffi', '#include <sha1.h>', libraries=['sha'])
