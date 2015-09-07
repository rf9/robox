from . import get_parsers

__author__ = 'dr6'


class RoboxParsingError(Exception):
    def __init__(self, *args, **kwargs):
        super(RoboxParsingError, self).__init__(*args, **kwargs)


def parse(file_to_parse):
    def fail(msg):
        raise RoboxParsingError("Error parsing file '%s': %s" % (file_to_parse, msg))

    parsers = get_parsers(file_to_parse)
    if not parsers:
        fail("No suitable parsers found.")
    if len(parsers) > 1:
        fail("Multiple possible parsers found.")
    parser = parsers[0]
    try:
        return {"data": list(parser.parse(file_to_parse)), "parser": parser.desc}
    except Exception as err:
        fail("An error %s was raised by parser %r" % (err, parser))
