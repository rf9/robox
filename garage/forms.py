from django import forms


class UploadFileForm(forms.Form):
    barcode = forms.CharField(label="Sample barcode")
    file = forms.FileField(label='Select file')

