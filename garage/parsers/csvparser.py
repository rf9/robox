from . import make_and_add_parser


def accept(f):
    return False # f.name.lower().endswith('.csv')


def parse(f):
    headings = None
    for bline in f:
        line = bline.decode('UTF-8').strip()
        if not line:
            headings = None
            continue
        parts = list(map(str.strip, line.split(',')))
        if not headings:
            headings = parts
        else:
            yield (list(zip(headings, parts)))


make_and_add_parser('CSV file with headers', parse, accept)
