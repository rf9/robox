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
    if len(barcode)==13 and barcode.isdigit():
        # EAN13
        total = sum(int(ch)*(1+2*(i&1)) for i,ch in enumerate(barcode[:-1]))
        checksum = (10-total)%10
        if str(checksum)==barcode[-1]:
            return
    raise ValidationError("Invalid barcode")


class UploadForm(forms.Form):
    barcode = BarcodeField()
    file = forms.FileField()
