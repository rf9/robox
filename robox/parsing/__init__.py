from collections import namedtuple as _namedtuple, OrderedDict as _OrderedDict
import importlib
import logging
import os

__author__ = 'dr6'

_Parser = _namedtuple('_Parser', 'desc parse accept')

_PARSERS = _OrderedDict()

_logger = logging.getLogger(__name__)


def add_parser(p):
    """
    Adds a parser object to the internal collection of parsers.

    The parameter <tt>p</tt> must provide the following attributes:
    <tt>desc</tt> a unique string describing the parser
    <tt>accept</tt> a boolean function that accepts a django file object and
    returns true if it is acceptable to this parser
    <tt>parse</tt> a function that accepts a django file object and yields
    lists of related key-value pairs parsed from the file
    """
    _logger.debug("Adding parser: %s" % p.desc)
    assert hasattr(p, 'desc')
    assert callable(p.accept)
    assert callable(p.parse)
    _PARSERS[p.desc] = p

def make_and_add_parser(desc, parse_function, accept_function=None):
    """
    Makes a parser object from the given parameters,
    and adds it to the internal collection of parsers.
    <tt>desc</tt> should uniquely identify the parser. If multiple parsers
    are registered with the same description, the last one added will
    replace all the others.
    <tt>parse</tt> must be a function that accepts a django file object and
    yields lists of related key/value pairs.
    <tt>accept</tt> should be a function that accepts a django file object and
    returns true or false depending on whether the file is suitable
    for this parser.
    :rtype : _Parser
    :param desc: A text description of this parser
    :type desc: str
    :param parse_function: A function to parse the file
    :param accept_function: A boolean function that predicts whether the given file is suitable
    :return: the parser added
    """
    p = _Parser(desc=desc, parse=parse_function, accept=accept_function)
    add_parser(p)
    return p


def get_parsers(file_to_parse=None):
    """
    Gets a list of parsers whose <tt>accept</tt> function returns true for the given
    django file object.
    If <tt>file_to_parse</tt> is not supplied, a list of all available parsers will be returned.
    :param file_to_parse: the file object we intend to parse
    :type file_to_parse: django.core.files.File
    :return: a list of matching parsers
    :rtype: list
    """
    if file_to_parse is None:
        return list(_PARSERS.values())
    return [p for p in _PARSERS.values() if p.accept(file_to_parse)]


for module in os.listdir(os.path.join(os.path.dirname(__file__), "parsers")):
    if module.endswith('.py') and module[0] not in '._':
        importlib.import_module('robox.parsing.parsers.' + module[:-3])


class RoboxParsingError(Exception):
    def __init__(self, *args, **kwargs):
        super(RoboxParsingError, self).__init__(*args, **kwargs)


def parse(file_to_parse):
    def fail(msg):
        raise RoboxParsingError("Error parsing file %r: %s" % (file_to_parse, msg))

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
