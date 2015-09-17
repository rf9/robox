from io import BytesIO
from plistlib import InvalidFileException
from zipfile import BadZipFile

import openpyxl

from robox.parsing import make_and_add_parser

desc = "xTen"


def accept(binary_file):
    try:
        file = openpyxl.load_workbook(BytesIO(binary_file))
        ws = file[file.get_sheet_names()[1]]

        for row in ws.rows:
            return [x.value for x in row] == ["Well\nRow", "Well\nCol", "Content", "Raw Data (485-12/EM520)",
                                              "Linear regression fit based on Raw Data (485-12/EM520)"]

    except (InvalidFileException, BadZipFile):
        return False

    return False


def parse(binary_file):
    file = openpyxl.load_workbook(BytesIO(binary_file))

    ws = file[file.get_sheet_names()[1]]

    first = True
    for row in ws.rows:
        if first:
            first = False
            continue

        slot = str(row[0].value) + str(row[1].value)
        concentration = row[4].value

        yield {"name": "concentration",
               "address": slot,
               "value": concentration,
               "units": "ng/ul"
               }


make_and_add_parser("xTen", parse, accept)
