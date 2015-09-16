import logging

from django import forms

from robox.utils import validate_barcode

_logger = logging.getLogger(__name__)


class BarcodeField(forms.Field):
    def to_python(self, value):
        return value

    def validate(self, value):
        validate_barcode(value)


class UploadForm(forms.Form):
    barcode = BarcodeField()
    file = forms.FileField()
