#
# https://getoutside.ordnancesurvey.co.uk/guides/beginners-guide-to-grid-references/
# https://en.wikipedia.org/wiki/Ordnance_Survey_National_Grid
#
import argparse
import math

from . import constants


def _tile_and_origin(
        easting: float, northing: float,
        tile_size: float) -> (str, float, float):
    tile_pos_n = math.floor(northing / tile_size)
    tile_pos_e = math.floor(easting / tile_size)

    letter = constants.LETTER_ORDER[tile_pos_e + 5 * tile_pos_n]
    origin_n = tile_pos_n * tile_size
    origin_e = tile_pos_e * tile_size

    return letter, origin_e, origin_n


def tile_500km(easting: float, northing: float):
    """Given easting and northing coordinates of a point
    in EPSG 27700, return the name of the 500km OS tile
    that contains that point.

    >>> tile_500km(212700, 770120)
    'N'
    """
    (letter, origin_e, origin_n) = _tile_and_origin(
        easting - constants.GRID_ORIGIN_SW_Easting,
        northing - constants.GRID_ORIGIN_SW_Northing, constants.TILE_1_SIZE)
    return letter


def _tile_100km_and_origin(easting: float, northing: float):
    (letter_1, origin_1_e, origin_1_n) = _tile_and_origin(
        easting - constants.GRID_ORIGIN_SW_Easting,
        northing - constants.GRID_ORIGIN_SW_Northing, constants.TILE_1_SIZE)
    (letter_2, origin_2_e, origin_2_n) = _tile_and_origin(
        easting - origin_1_e - constants.GRID_ORIGIN_SW_Easting,
        northing - origin_1_n - constants.GRID_ORIGIN_SW_Northing,
        constants.TILE_2_SIZE)
    letters = letter_1 + letter_2
    origin_e = origin_1_e + origin_2_e + constants.GRID_ORIGIN_SW_Easting
    origin_n = origin_1_n + origin_2_n + constants.GRID_ORIGIN_SW_Northing
    return letters, origin_e, origin_n


def tile_100km(easting: float, northing: float) -> str:
    """Given easting and northing coordinates of a point
    in EPSG 27700, return the name of the 100km OS tile
    that contains that point.

    >>> tile_100km(212700, 770120)
    'NN'
    """
    letters, origin_e, origin_n = _tile_100km_and_origin(easting, northing)
    return letters


def tile_n(easting: float, northing: float, nb_digits: int) -> str:
    """Given easting and northing coordinates of a point
    in EPSG 27700, return the name of the 'numbers'-numbers
    OS tile that contains that point

    :param easting: easting of the point
    :param northing: northing of the point
    :param nb_digits: number of digits expected in the OS tile name
    :return: the corresponding OS tile name
    """

    if nb_digits <= 0 or nb_digits % 2 != 0:
        raise ValueError("The number of digits should be even")

    letters, origin_e, origin_n = _tile_100km_and_origin(easting, northing)
    tile_side = 100_000 / 10**(nb_digits//2)
    coord_e = math.floor((easting - origin_e) / tile_side)
    coord_n = math.floor((northing - origin_n) / tile_side)
    # format string may have numbers / 2 zeros
    fs = "%" + "0%i" % (nb_digits // 2) + "i"

    return ("%s" + fs + fs) % (letters, coord_e, coord_n)


def tile_10km(easting: float, northing: float) -> str:
    """Given easting and northing coordinates of a point
    in EPSG 27700, return the name of the 10km OS tile
    that contains that point.

    >>> tile_10km(212700, 770120)
    'NN17'
    """
    return tile_n(easting, northing, 2)


def tile_1km(easting: float, northing: float) -> str:
    """Given easting and northing coordinates of a point
    in EPSG 27700, return the name of the 1km OS tile
    that contains that point.
    >>> tile_1km(212700, 770120)
    'NN1270'
    """

    return tile_n(easting, northing, 4)


def tile_100m(easting: float, northing: float) -> str:
    """Given easting and northing coordinates of a point
    in EPSG 27700, return the name of the 100m OS tile
    that contains that point.

    >>> tile_100m(212700, 770120)
    'NN127701'
    """
    return tile_n(easting, northing, 6)


def tile_10m(easting: float, northing: float) -> str:
    """Given easting and northing coordinates of a point
    in EPSG 27700, return the name of the 10m OS tile
    that contains that point.

    >>> tile_10m(212700, 770120)  # Dun Deardail
    'NN12707012'
    """
    return tile_n(easting, northing, 8)


def tile_1m(easting: float, northing: float) -> str:
    """Given easting and northing coordinates of a point
    in EPSG 27700, return the name of the 1m OS tile
    that contains that point.

    """
    return tile_n(easting, northing, 10)


def main():

    functions = {
        "1m": tile_1m,
        "10m": tile_10m,
        "100m": tile_100m,
        "1km": tile_1km,
        "10km": tile_10km,
    }

    parser = argparse.ArgumentParser(
        description="Encode OS Grid Reference ")
    parser.add_argument("--easting", type=float,
                        required=True, help="Easting")
    parser.add_argument("--northing", type=float,
                        required=True, help="Northing")
    parser.add_argument("--size", choices=functions.keys(),
                        default="1km", help="Tile size")

    arguments = parser.parse_args()

    tile_id = functions[arguments.size](arguments.easting, arguments.northing)
    print(tile_id)


if __name__ == "__main__":
    main()
