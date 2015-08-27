from django import forms


class UploadForm(forms.Form):
    barcode = forms.CharField()
    file = forms.FileField()
