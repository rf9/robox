from robox.parsers.FileData import FileData


def parse(file_path):
    try:
        file = open(file_path)

        data = FileData()

        first = True
        for line in file:
            if first:
                line = [x for x in filter(None, line.replace("\n", "").split(","))]
                if line != ['Plate Name', 'Well Label', 'Sample Name', 'Peak Count', 'Total Conc. (ng/ul)',
                            'EP138 Molarity (nmol/l)', 'Region[200-1400] Size at Maximum [BP]',
                            'Region[200-1400] Size [BP]', 'Region[200-1400] Molarity (nmol/l)']:
                    return None
                first = False
                continue

            line = line.replace("\n", "")

            cells = line.split(",")
            slot = cells[2].split("_")[0]
            concentration = cells[8]
            dilution_parts = cells[2].split("_")[-2:]

            try:
                dilution = int(dilution_parts[0]) / int(dilution_parts[1]) * 100
            except ValueError:
                dilution = None

            if concentration:
                data.add_entry("concentration", slot, concentration, "nM")
            if dilution:
                data.add_entry("dilution", slot, dilution, "%")
    except UnicodeDecodeError:
        return None

    return data
