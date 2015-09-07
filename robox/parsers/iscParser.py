from . import make_and_add_parser


def accept(file):
    try:
        for line in file:
            cells = line.decode('ascii').replace("\n", "").split(",")
            return [x for x in filter(None, cells)] == ['Plate Name', 'Well Label', 'Sample Name', 'Peak Count',
                                                        'Total Conc. (ng/ul)', 'Region[200-700] Molarity (nmol/l)']
    except UnicodeDecodeError:
        return False


def parse(file):
    first = True
    for line in file:
        if first:
            first = False
            continue

        cells = line.decode('ascii').replace("\n", "").split(",")

        slot = cells[2].split("_")[0]
        concentration = cells[5]
        dilution_parts = cells[2].split("_")[-2:]

        try:
            dilution = int(dilution_parts[0]) / int(dilution_parts[1]) * 100
        except ValueError:
            dilution = None

        if concentration:
            yield {"name": "concentration",
                   "address": slot,
                   "value": concentration,
                   "units": "nM"
                   }

        if dilution:
            yield {"name": "dilution",
                   "address": slot,
                   "value": dilution,
                   "units": "%"
                   }


make_and_add_parser("isc", parse, accept)
