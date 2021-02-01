import math
import enum
from typing import Dict
ADDRESS_SIZE = 64


def address_to_bits(address: int) -> tuple:
    bits = []
    for i_bit in range(ADDRESS_SIZE):
        bit = int(address % 2 == 1)
        bits.append(bit)
        address //= 2
    return tuple(bits)


class LookupResult(enum.Enum):
    Hit = 0
    Miss = 1


class SetLine:
    def __init__(self, n_ways):
        self.n_ways = n_ways
        self.valid = [False] * n_ways
        self.tags = [None] * n_ways
        self.order = list(range(n_ways))

    def _search(self, tag):
        for i in range(self.n_ways):
            if self.valid[i] and self.tags[i] == tag:
                return i
        return None

    def _empty_space(self):
        for i in range(self.n_ways):
            if not self.valid[i]:
                return i
        return None

    def _choose_victim(self):
        return self.order[-1]

    def _update_lru(self, way):
        self.order.remove(way)
        self.order = [way] + self.order

    def lookup(self, tag) -> LookupResult:
        # check if the tag is present
        way = self._search(tag)
        if way is not None:
            self._update_lru(way)
            return LookupResult.Hit
        # check if there is empty space
        way = self._empty_space()
        if way is not None:
            self.tags[way] = tag
            self.valid[way] = True
            self._update_lru(way)
            return LookupResult.Miss
        # choose a victim and replace
        way = self._choose_victim()
        self.tags[way] = tag
        self._update_lru(way)
        return LookupResult.Miss


class Cache:
    def __init__(self, size, ways, block_size):
        self.size = size
        self.n_ways = ways
        self.block_size = block_size
        self.n_blocks = self.size // self.block_size
        self.n_sets = self.n_blocks // self.n_ways

        # number of bits
        self.offset_bits = int(math.log2(self.block_size))
        self.set_bits = int(math.log2(self.n_sets))

        # state of the sets
        self.set_lines: Dict[tuple, SetLine] = {}

    def lookup(self, address) -> LookupResult:
        bits = address_to_bits(address)
        set = bits[self.offset_bits:self.offset_bits + self.set_bits]
        tag = bits[self.offset_bits + self.set_bits:ADDRESS_SIZE]

        if set not in self.set_lines:
            self.set_lines[set] = SetLine(self.n_ways)

        return self.set_lines[set].lookup(tag)


def win_2017_a_2_b():
    data_cache = Cache(2 ** 14, 2, 2 ** 6)
    base_address = 0x800_000
    row_offset = 1600
    col_offset = 8
    total = 0
    hit = 0
    for k in range(1, 11):
        for i in range(0, 100):
            for j in range(0, 200):
                total += 1
                address = base_address + row_offset * i + col_offset * j
                res = data_cache.lookup(address)
                if res == LookupResult.Hit:
                    hit += 1

    print(f"HR={hit / total}")


def win_2017_a_2_c():
    data_cache = Cache(2 ** 14, 2, 2 ** 6)
    base_address = 0x800_000
    row_offset = 1600
    col_offset = 8
    total = 0
    hit = 0

    for k in range(1, 11):
        for j in range(0, 200):
            for i in range(0, 100):

                total += 1
                address = base_address + row_offset * i + col_offset * j
                res = data_cache.lookup(address)
                if res == LookupResult.Hit:
                    hit += 1

    print(f"HR={hit / total}")


if __name__ == "__main__":
    win_2017_a_2_c()


