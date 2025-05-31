# sprite.py

def decode_tile(tile_bytes):
    output = []
    for i in range(0, len(tile_bytes), 2):
        low = tile_bytes[i]
        high = tile_bytes[i+1]
        row = ''
        for bit in range(7, -1, -1):
            lo_bit = (low >> bit) & 1
            hi_bit = (high >> bit) & 1
            val = (hi_bit << 1) | lo_bit
            row += str(val)
        output.append(row)
    return output



def encode_tile(ascii_rows):
    tile_bytes = []
    for row in ascii_rows:
        low_byte = 0
        high_byte = 0
        for i, ch in enumerate(row):
            val = int(ch)  # 0 to 3
            lo_bit = val & 1
            hi_bit = (val >> 1) & 1
            bit_pos = 7 - i
            low_byte |= (lo_bit << bit_pos)
            high_byte |= (hi_bit << bit_pos)
        tile_bytes.append(low_byte)
        tile_bytes.append(high_byte)
    return tile_bytes

def print_ascii_dither(tile_rows):
    pixel_map = {
        '0': '  ',
        '1': '░░',  # ░
        '2': '▒▒',  # ▒
        '3': '▓▓',  # ▓
    }
    for row in tile_rows:
        print("".join(pixel_map[ch] for ch in row))




tile_data = [
    0x00, 0x00, 0x00, 0x00, 0x3C, 0x3C, 0x5E, 0x62,
    0xBF, 0xC1, 0xBF, 0xD3, 0xBF, 0xC1, 0xBF, 0xC1,
]

ascii_tiles = decode_tile(tile_data)
ascii_tiles_ = [
    '00000000',
    '00000000',
    '00333300',
    '03100030',
    '31000003',
    '31030033',
    '31000003',
    '31000003'
]

print_ascii_dither(ascii_tiles_)
hex_p = encode_tile(ascii_tiles_)
print(hex_p)

def hex_string(tile_bytes):
    return ', '.join(f'0x{b:02X}' for b in tile_bytes)

def print_c_array(tile_bytes, name="tile_data"):
    print(f"unsigned char {name}[] = {{")
    print("  " + ", ".join(f"0x{b:02X}" for b in tile_bytes))
    print("};")



hex_p = encode_tile(ascii_tiles_)
print("Tile bytes in hex:")
print(hex_string(hex_p))

print_c_array(hex_p, "my_tile")
