import struct
import bitstring


def p8(v):
    return bytes([v])

def p16(v):
    return struct.pack('>H', v)

def p32(v):
    return struct.pack('>I', v)

def p64(v):
    return struct.pack('>Q', v)

def u8(v):
    first, = list(v)
    return first

def u16(v):
    return struct.unpack('>H', v)[0]

def u32(v):
    return struct.unpack('>I', v)[0]

def u64(v):
    return struct.unpack('>Q', v)[0]

