__author__ = 'rf9'

from robox.parsers import iscParser, wgsParser, xTenParser


def get_parsers():
    return [
        (iscParser, "isc"),
        (wgsParser, "wgs"),
        (xTenParser, "xTen"),
    ]
