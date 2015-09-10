from parsing import make_and_add_parser

desc = "wgs"


def accept(file):
    try:
        for line in file:
            cells = line.decode('ascii').rstrip('\n').split(",")
            return [x for x in filter(bool, cells)] == ['Plate Name', 'Well Label', 'Sample Name', 'Peak Count',
                                                        'Total Conc. (ng/ul)', 'EP138 Molarity (nmol/l)',
                                                        'Region[200-1400] Size at Maximum [BP]',
                                                        'Region[200-1400] Size [BP]',
                                                        'Region[200-1400] Molarity (nmol/l)']
    except UnicodeDecodeError:
        return False


def parse(file):
    first = True
    for line in file:
        if first:
            first = False
            continue

        cells = line.decode('ascii').rstrip('\n').split(",")

        slot = cells[2].split("_")[0]
        concentration = cells[8]
        dilution_parts = cells[2].split("_")[-2:]

        if concentration:
            yield {"name": "concentration",
                   "address": slot,
                   "value": concentration,
                   "units": "nM"
                   }

        try:
            dilution = int(dilution_parts[0]) / int(dilution_parts[1]) * 100
        except ValueError:
            dilution = None

        if dilution is not None:
            yield {"name": "dilution",
                   "address": slot,
                   "value": dilution,
                   "units": "%"
                   }


make_and_add_parser("wgs", parse, accept)
