from zipfile import BadZipFile
import openpyxl
from openpyxl.utils.exceptions import InvalidFileException
from robox.parsers.FileData import FileData


def parse(file_path):
    try:
        file = openpyxl.load_workbook(file_path)
    except (InvalidFileException, BadZipFile):
        return None

    ws = file[file.get_sheet_names()[1]]
    data = FileData()

    first = True
    for row in ws.rows:
        if first:
            first = False
            continue

        slot = str(row[0].value) + str(row[1].value)
        concentration = row[4].value

        data.add_entry("concentration", slot, concentration, "ng/ul")

    return data
