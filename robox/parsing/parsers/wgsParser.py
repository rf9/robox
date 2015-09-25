from collections import OrderedDict

from robox.parsing import make_and_add_parser

desc = "wgs"


def accept(file):
    try:
        for line in file.decode('ascii').split('\n'):
            cells = line.split(",")
            return [x for x in filter(bool, cells)] == ['Plate Name', 'Well Label', 'Sample Name', 'Peak Count',
                                                        'Total Conc. (ng/ul)', 'EP138 Molarity (nmol/l)',
                                                        'Region[200-1400] Size at Maximum [BP]',
                                                        'Region[200-1400] Size [BP]',
                                                        'Region[200-1400] Molarity (nmol/l)']
    except UnicodeDecodeError:
        return False


def parse(file):
    first = True
    for line in file.decode('ascii').split('\n'):
        if first:
            first = False
            continue
        if not line:
            continue
        cells = line.split(",")

        slot = cells[2].split("_")[0]
        concentration = cells[8]
        dilution_parts = cells[2].split("_")[-2:]

        if concentration:
            yield OrderedDict((
                ('address', slot),
                ('name', 'concentration'),
                ('value', concentration),
                ('units', 'nM')
            ))

        try:
            dilution = int(dilution_parts[0]) / int(dilution_parts[1]) * 100
        except ValueError:
            dilution = None

        if dilution:
            yield OrderedDict((
                ('address', slot),
                ('name', "dilution"),
                ('value', dilution),
                ('units', "%")
            ))


make_and_add_parser("wgs", parse, accept)
