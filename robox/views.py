from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView

from robox.forms import UploadForm
from robox.models import File, Entry, MetaData
from robox.parsers import get_parsers


class UploadView(FormView):
    template_name = "robox/upload.html"
    form_class = UploadForm

    def form_valid(self, form):

        file = self.get_form_kwargs().get('files')['file']
        datas = []
        parser_name = "None"
        parsers = get_parsers()
        for (parser, name) in parsers:
            file_data = parser.parse(file)
            if file_data is not None:
                datas.append(file_data)
                parser_name = name

        data_base_file = File.objects.create(
            file=file,
            barcode=form.cleaned_data['barcode'],
            format=parser_name,
        )

        if len(datas) == 1:
            for data in datas[0].data:
                entry = Entry.objects.create(file=data_base_file, value=data.value)
                for key in data.meta:
                    MetaData.objects.create(entry=entry, key=key, value=data.meta[key])

        return HttpResponseRedirect(reverse('view', kwargs={'barcode': data_base_file.barcode}))


def view(request, barcode):
    rows = []
    for entry in Entry.objects.filter(file__barcode=barcode):
        row = ["", "", entry.value, ""]
        for datum in entry.metadata_set.all():
            if datum.key == "address":
                row[0] = datum.value
            elif datum.key == "name":
                row[1] = datum.value
            elif datum.key == "units":
                row[3] = datum.value
        rows.append(row)

    return render(request, "robox/view.html", {"rows": rows})
