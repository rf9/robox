__author__ = 'dr6'

from .parsers import get_parsers
from .models import File, Item, Data


class GarageParsingError(Exception):
    def __init__(self, *args, **kwargs):
        super(GarageParsingError, self).__init__(*args, **kwargs)


def parse(filetoparse):
    def fail(msg):
        raise GarageParsingError("Error parsing file '%s': %s" % (filetoparse, msg))

    parsers = get_parsers(filetoparse)
    if not parsers:
        fail("No suitable parsers found.")
    if len(parsers) > 1:
        fail("Multiple possible parsers found.")
    parser = parsers[0]
    try:
        return list(parser.parse(filetoparse))
    except Exception:
        fail("An error was raised by parser %r" % parser)
