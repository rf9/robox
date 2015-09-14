import logging

from django import forms
from django.core.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class BarcodeField(forms.Field):
    def to_python(self, value):
        return value

    def validate(self, value):
        validate_barcode(value)


def validate_barcode(barcode):
    """
    Validate the barcode against EAN13 format.
    :raises ValidationError: if barcode is not valid.
    :param barcode: The barcode to be validated
    """

    if barcode.isdigit() and len(barcode) == 13:
        # EAN13
        checksum = 0
        for i in range(12):
            if i % 2 == 0:
                checksum += int(barcode[i])
            else:
                checksum += int(barcode[i]) * 3

        if ((10 - checksum) % 10) == int(barcode[12]):
            return

    raise ValidationError("Invalid barcode")


class UploadForm(forms.Form):
    barcode = BarcodeField()
    file = forms.FileField()
