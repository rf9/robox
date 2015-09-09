import re
import string

from django import forms
from django.core.exceptions import ValidationError


class BarcodeField(forms.Field):
    def to_python(self, value):
        return value.upper()

    def validate(self, value):
        validate_barcode(value)


def validate_barcode(barcode):
    """
    Validate the barocode against Barcode39, EAN13, and EBI formats.
    :raises ValidationError: if barcode is not valid.
    :param barcode: The barcode to be validated
    :return: None if valid.
    """
    barcode = barcode.upper()

    if re.match(r'^[0-9A-Z\*]{2,}$', barcode) is not None:
        # Barcode39
        checksum = 0
        alphabet = string.digits + string.ascii_uppercase + '*'
        for i in range(len(barcode) - 1):
            checksum += alphabet.find(barcode[i]) << (len(barcode) - 1 - i)

        if alphabet[(38 - (checksum % 37)) % 37] == barcode[-1]:
            return
    if re.match(r'^[0-9]{13}$', barcode) is not None:
        # EAN13
        checksum = 0
        for i in range(12):
            if i % 2 == 0:
                checksum += int(barcode[i]) * 3
            else:
                checksum += int(barcode[i])

        if ((10 - checksum) % 10) == int(barcode[12]):
            return
    if re.match(r'^SAMEA[0-9]{7}$', barcode):
        # EBI
        return

    raise ValidationError("Invalid barcode")


class UploadForm(forms.Form):
    barcode = BarcodeField()
    file = forms.FileField()
