from zipfile import BadZipFile
import openpyxl
from openpyxl.utils.exceptions import InvalidFileException
from . import make_and_add_parser

desc = "xTen"


def accept(file_path):
    try:
        file = openpyxl.load_workbook(file_path)
    except (InvalidFileException, BadZipFile):
        return False

    return True


def parse(file_path):
    file = openpyxl.load_workbook(file_path)

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
