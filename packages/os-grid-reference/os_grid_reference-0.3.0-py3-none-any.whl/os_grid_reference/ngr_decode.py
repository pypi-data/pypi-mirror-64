import argparse
import json
from typing import NamedTuple
import re

from . import constants


class Tile(NamedTuple):
    # Coordinates of the south-west point of the tile
    sw_easting: float
    sw_northing: float
    # Coordinates of the north-east point of the tile
    ne_easting: float
    ne_northing: float
    # Size of the tile, in meters
    size: float

    @staticmethod
    def create(sw_easting: float, sw_northing: float, size: float) -> "Tile":
        return Tile(sw_easting, sw_northing,
                    sw_easting + size, sw_northing + size, size)

    def __repr__(self):
        return f"<Tile sw_easting={self.sw_easting} " \
               f"sw_northing={self.sw_northing} " \
               f"size={self.size}>"

    def as_dict(self) -> dict:
        """Return the tile geometry as a dictionary"""
        return {
            "sw_easting": self.sw_easting,
            "sw_northing": self.sw_northing,
            "ne_easting": self.ne_easting,
            "ne_northing": self.ne_northing,
            "size": self.size,
        }

    def as_wkt(self) -> str:
        """Return the tile geometry as Well Known Text string"""
        coords = [
            (self.sw_easting, self.sw_northing),
            (self.ne_easting, self.sw_northing),
            (self.ne_easting, self.ne_northing),
            (self.sw_easting, self.ne_northing),
            (self.sw_easting, self.sw_northing),
        ]
        return "POLYGON ((%s))" % ", ".join([
            "%s %s" % (x, y) for (x, y) in coords
        ])


def _split_tile_id_and_validate(tile_id: str):
    prefix, s1, s2, suffix = _split_tile_id(tile_id)
    if suffix not in (None, "NE", "NW", "SE", "SW"):
        raise ValueError("Incorrect format #1")

    depth = len(s1 or '')
    n1 = int(s1) if s1 is not None else None
    n2 = int(s2) if s1 is not None else None

    if len(prefix) == 1 and n1 is not None:
        raise ValueError("Incorrect format #2")
    elif len(prefix) > 2 or len(prefix) == 0:
        raise ValueError("Incorrect format #3")

    return prefix, depth, n1, n2, suffix


def _handle_suffix(orig_e, orig_n, tile_size, suffix) -> Tile:
    if suffix is None:
        return Tile.create(orig_e, orig_n, tile_size)

    half_tile = tile_size / 2
    if suffix == 'SW':
        return Tile.create(orig_e, orig_n, half_tile)
    elif suffix == 'SE':
        return Tile.create(orig_e + half_tile, orig_n, half_tile)
    elif suffix == 'NW':
        return Tile.create(orig_e, orig_n + half_tile, half_tile)
    elif suffix == 'NE':
        return Tile.create(orig_e + half_tile, orig_n + half_tile, half_tile)


def ngr_decode(tile_id: str) -> Tile:
    """Given a tile name, return the corresponding box

    >>> ngr_decode("HU396753")
    <Tile sw_easting=439600.0 sw_northing=1175300.0 size=100.0>
    """
    prefix, depth, n1, n2, suffix = _split_tile_id_and_validate(tile_id)
    letter_1_idx = constants.LETTER_ORDER.index(prefix[0])

    orig_n = (constants.TILE_1_SIZE * (letter_1_idx // 5)
              + constants.GRID_ORIGIN_SW_Northing)
    orig_e = (constants.TILE_1_SIZE * (letter_1_idx % 5)
              + constants.GRID_ORIGIN_SW_Easting)

    if len(prefix) == 1:
        return _handle_suffix(orig_e, orig_n, constants.TILE_1_SIZE, suffix)

    letter_2_idx = constants.LETTER_ORDER.index(prefix[1])
    orig_n += constants.TILE_2_SIZE * (letter_2_idx // 5)
    orig_e += constants.TILE_2_SIZE * (letter_2_idx % 5)

    if n1 is None:
        return _handle_suffix(orig_e, orig_n, constants.TILE_2_SIZE, suffix)

    cell_size = constants.TILE_2_SIZE / 10**depth
    orig_e += n1 * cell_size
    orig_n += n2 * cell_size

    return _handle_suffix(orig_e, orig_n, cell_size, suffix)


def _split_tile_id(_tile_id: str):
    """
    cases:
        A
        AB
        ASW!
        ABSW!
        AB12NE
        AB1124NE
        AB112242NE
    :param tile_id:
    :return:
    """
    tile_id = _tile_id.upper()
    reg = re.compile(r"^(?P<prefix>[A-Z]+)(?P<numbers>\d*)(?P<suffix>[A-Z]*)$")
    match = reg.match(tile_id)
    if match is None:
        raise ValueError("Incorrect format")

    prefix = match.group("prefix")

    # nb_prefix_letters = itertools.takewhile(lambda s: s.isalpha(), tile_id)
    if len(prefix) != 2:
        # Cases with no numbers
        if len(tile_id) != len(prefix):
            raise ValueError("Not a valid tile id")
        elif len(prefix) == 1:
            return tile_id, None, None, None
        elif len(prefix) == 3:
            tile = tile_id[0]
            suffix = tile_id[1:]
            return tile, None, None, suffix
        elif len(prefix) == 4:
            tile = tile_id[:2]
            suffix = tile_id[2:]
            return tile, None, None, suffix
        else:
            raise ValueError("Not a valid tile id #2")
    else:
        tile = tile_id[:2]
        numbers = match.group("numbers")
        if len(numbers) % 2 != 0:
            raise ValueError("Not a valid tile id #3")
        split = len(numbers) // 2
        n1 = numbers[:split] or None
        n2 = numbers[split:] or None

        suffix = match.group("suffix") or None
        return tile, n1, n2, suffix


def main():
    parser = argparse.ArgumentParser(
        description="Decode OS Grid Reference tile names")
    parser.add_argument("tile_name", type=str,
                        help="Tile name (e.g. HU396753)")
    parser.add_argument('--as-wkt', action="store_true",
                        help="Output result as WKT")

    arguments = parser.parse_args()
    tile = ngr_decode(arguments.tile_name)

    if not arguments.as_wkt:
        print(json.dumps(tile.as_dict(), indent=4))
    else:
        print(tile.as_wkt())


if __name__ == "__main__":
    main()
