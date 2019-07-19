import struct
import zlib
from utils import p32, p8
IHDR = b'IHDR'
IDAT = b'IDAT'
IEND = b'IEND'

COLOR_TYPE = {
    'rgb': 2,
    'grayscale': 0,
}


def make_png_chunk(name, data):
    return p32(len(data)) + name + data + p32(zlib.crc32(name + data))


def make_ihdr_data(width, height, bit_depth=8, color_type='rgb', comp_meth=0, filt_meth=0, inter_meth=0):
    d = p32(width) + p32(height)
    d += p8(bit_depth) + p8(COLOR_TYPE[color_type]) 
    d += p8(comp_meth)
    d += p8(filt_meth)
    d += p8(inter_meth)
    assert len(d) == 13
    return d

def make_ihdr_chunk(width, height):
    return make_png_chunk(IHDR, make_ihdr_data(width, height))

def make_iend_chunk():
    return make_png_chunk(IEND, b'')

PNG_MAGIC = bytes(bytearray([137, 80, 78, 71, 13, 10, 26, 10])) # magic
def make_png(data_chunks, width=100, height=100):
    d = b''
    d += PNG_MAGIC
    d + make_ihdr_chunk(width, height)
    d += b''.join(make_png_chunk(IDAT, c) for c in data_chunks)
    d += make_iend_chunk()
    return d
