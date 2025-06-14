class Sprite:
    def __init__(self, name="unnamed"):
        self.name = name
        self.tiles = {}  # { tile_id: [ascii_rows] }

    @staticmethod
    def decode_tile(tile_bytes):
        output = []
        for i in range(0, len(tile_bytes), 2):
            low = tile_bytes[i]
            high = tile_bytes[i + 1]
            row = ''
            for bit in range(7, -1, -1):
                lo_bit = (low >> bit) & 1
                hi_bit = (high >> bit) & 1
                val = (hi_bit << 1) | lo_bit
                row += str(val)
            output.append(row)
        return output

    @staticmethod
    def encode_tile(ascii_rows):
        tile_bytes = []
        for row in ascii_rows:
            low_byte = 0
            high_byte = 0
            for i, ch in enumerate(row):
                val = int(ch)  # 0–3
                lo_bit = val & 1
                hi_bit = (val >> 1) & 1
                bit_pos = 7 - i
                low_byte |= (lo_bit << bit_pos)
                high_byte |= (hi_bit << bit_pos)
            tile_bytes.append(low_byte)
            tile_bytes.append(high_byte)
        return tile_bytes

    def add_tile(self, tile_id, ascii_rows):
        self.tiles[tile_id] = ascii_rows

    def get_tile_no(self):
        pass

    def get_tile_bytes(self):
        result = []
        for tile_id in sorted(self.tiles.keys()):
            result.extend(self.encode_tile(self.tiles[tile_id]))
        return result

    def print_ascii(self):
        pixel_map = {
            '0': '  ',
            '1': '░░',
            '2': '▒▒',
            '3': '▓▓',
        }
        for tile_id in sorted(self.tiles.keys()):
            print(f"Tile {tile_id}:")
            for row in self.tiles[tile_id]:
                print("".join(pixel_map[ch] for ch in row))
            print()

    def get_c_array(self, varname="tile_data"):
        tile_bytes = self.get_tile_bytes()
        code = ''
        code += f"unsigned char {varname}[] = {{"
        code += "  " + ", ".join(f"0x{b:02X}" for b in tile_bytes)
        code += "};"

        return code

    @classmethod
    def from_file(cls, path):
        sprite = cls()
        with open(path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        current_tile = None
        tile_rows = []

        for line in lines:
            if line.startswith('name:'):
                sprite.name = line.split(':', 1)[1].strip()
            elif line.endswith(':') and line[:-1].isdigit():
                if current_tile is not None:
                    sprite.tiles[current_tile] = tile_rows
                current_tile = int(line[:-1])
                tile_rows = []
            elif all(c in '0123' for c in line) and len(line) == 8:
                tile_rows.append(line)

        if current_tile is not None:
            sprite.tiles[current_tile] = tile_rows

        return sprite


#sprite = Sprite.from_file("examples/sprite.gbspr")

#sprite.print_ascii()
#print(sprite.get_c_array("slime_tiles"))
