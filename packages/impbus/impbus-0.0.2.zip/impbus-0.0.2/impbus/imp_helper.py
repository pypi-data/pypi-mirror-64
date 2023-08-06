# -*- coding: UTF-8 -*-


def _normalize(filename):
    """ .. function:: _normalize(filename)

    Prepends the filename with the path pointing to the main file.

    :type filename: string
    :rtype: string
    """
    import os
    abs_path = os.path.abspath(__file__)
    dir_name = os.path.dirname(abs_path)
    return os.path.join(dir_name, filename)


def _load_json(filename):
    """ .. funktion:: _load_json(filename)

    Reads the spezific json file.

    :type filename: string
    :rtype: dict
    """
    import json
    filename = _normalize(filename)
    with open(filename) as js_file:
        return json.load(js_file)


def _flp2(number):
    """ .. funktion:: _flp2(number)

    Rounds x to the largest z | z=2**n.

    :type number: int
    :rtype: int
    """
    number |= (number >> 1)
    number |= (number >> 2)
    number |= (number >> 4)
    number |= (number >> 8)
    number |= (number >> 16)
    return number - (number >> 1)


def _imprange(low, high):
    """ .. funktion:: _imprange(low, high)

    Takes a serial number range and returns the range address and the marker
    which can be compined (range + maker) to the broadcast address for the
    given range.

    :type low: int
    :type high: int
    :rtype: tuble

    """
    pfix = low ^ high
    mark = _flp2(pfix)
    fill = mark | (mark - 1)
    mask = fill ^ 0xFFFFFF
    return low & mask, mark
