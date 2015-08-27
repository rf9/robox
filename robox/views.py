from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.views.generic import FormView

from robox.forms import UploadForm
from robox.models import File, Entry, MetaData


# Create your views here.
class UploadView(FormView):
    template_name = "robox/upload.html"
    form_class = UploadForm

    def form_valid(self, form):
        data_base_file = File(
            file=self.get_form_kwargs().get('files')['file'],
            barcode=form.cleaned_data['barcode']
        )

        data_base_file.save()

        first = True
        for line in data_base_file.file:
            if first:
                first = False
                continue

            line = str(line)
            line = line.replace("\\n", "")

            cells = line.split(",")

            slot = cells[2].split("_")[0]
            try:
                concentration = float(cells[5].replace("'", ""))
            except ValueError:
                concentration = None

            dilution_parts = cells[2].split("_")[-2:]
            try:
                dilution = int(dilution_parts[0]) * 100 / int(dilution_parts[1])
            except ValueError:
                dilution = None

            if concentration is not None:
                entry = Entry(file=data_base_file, value=concentration)
                entry.save()
                MetaData(entry=entry, key="slot", value=slot).save()
                MetaData(entry=entry, key="measurement", value="concentration").save()
                MetaData(entry=entry, key="units", value="nM").save()
            if dilution is not None:
                entry = Entry(file=data_base_file, value=dilution)
                entry.save()
                MetaData(entry=entry, key="slot", value=slot).save()
                MetaData(entry=entry, key="measurement", value="dilution").save()
                MetaData(entry=entry, key="units", value="%").save()

        return HttpResponseRedirect(reverse('view', kwargs={'barcode': data_base_file.barcode}))


def view(request, barcode):
    # return HttpResponse("<br/>".join([str(x.value) for x in Entry.objects.filter(file__barcode=barcode)]))
    rows = []
    for entry in Entry.objects.filter(file__barcode=barcode):
        row = ["", "", entry.value, ""]
        for datum in entry.metadata_set.all():
            if datum.key == "slot":
                row[0] = datum.value
            elif datum.key == "measurement":
                row[1] = datum.value
            elif datum.key == "units":
                row[3] = datum.value
        rows.append(row)

    return render(request, "robox/view.html", {"rows": rows})
