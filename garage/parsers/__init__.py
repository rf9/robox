from collections import namedtuple as _namedtuple, OrderedDict as _OrderedDict
import importlib

__author__ = 'dr6'

_Parser = _namedtuple('_Parser', 'desc parse accept')

_PARSERS = _OrderedDict()


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
    print("Adding parser:", p.desc)
    assert hasattr(p, 'desc')
    assert callable(p.accept)
    assert callable(p.parse)
    _PARSERS[p.desc] = p


def make_and_add_parser(desc, parse, accept=None):
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
    for this parser. If accept is None, any file will be accepted.
    :rtype : _Parser
    :param desc: A text description of this parser
    :type desc: str
    :param parse: A function to parse the file
    :param accept: A boolean function that predicts whether the given file is suitable
    :return: the parser added
    """
    if accept is None:
        accept = lambda x: True
    p = _Parser(desc=desc, parse=parse, accept=accept)
    add_parser(p)
    return p


def get_parsers(filetoparse=None):
    """
    Gets a list of parsers whose <tt>accept</tt> function returns true for the given
    django file object.
    If <tt>filetoparse</tt> is not supplied, a list of all available parsers will be returned.
    :param filetoparse: the file object we intend to parse
    :type filetoparse: django.core.files.File
    :return: a list of matching parsers
    :rtype: list
    """
    if filetoparse is None:
        return list(_PARSERS.values())
    return [p for p in _PARSERS.values() if p.accept(filetoparse)]


import os

for module in os.listdir(os.path.dirname(__file__)):
    if module.endswith('.py') and module[0] not in '._':
        importlib.import_module('garage.parsers.' + module[:-3])

del os
