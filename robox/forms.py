import re
import string

from django import forms
from django.core.exceptions import ValidationError


class BarcodeField(forms.Field):
    def to_python(self, value):
        return value.upper()

    def validate(self, value):
        if re.match(r'^[0-9A-Z\*]{2,}$', value) is not None:
            # Barcode39
            checksum = 0
            alphabet = string.digits + string.ascii_uppercase + '*'
            for i in range(len(value) - 1):
                checksum += alphabet.find(value[i]) << (len(value) - 1 - i)

            if alphabet[(38 - (checksum % 37)) % 37] == value[-1]:
                return
        if re.match(r'^[0-9]{13}$', value) is not None:
            # EAN13
            checksum = 0
            for i in range(12):
                if i % 2 == 0:
                    checksum += int(value[i]) * 3
                else:
                    checksum += int(value[i])

            if ((10 - checksum) % 10) == int(value[12]):
                return
        if re.match(r'^SAMEA[0-9]{7}$', value):
            # EBI
            return

        raise ValidationError("Invalid barcode")


class UploadForm(forms.Form):
    barcode = BarcodeField()
    file = forms.FileField()
