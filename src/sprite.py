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


ascii_tile = [
    "00000000",
    "11111111",
    "22222222",
    "33333333",
    "01230123",
    "32103210",
    "00001111",
    "11110000"
]

gb_bytes = encode_tile(ascii_tile)
print([f"0x{b:02X}" for b in gb_bytes])
