from django.utils import timezone

from .models import File, Item, Data

__author__ = 'dr6'


def record(barcode, filename, rows):
    f = File(barcode=barcode, filename=filename, upload_date=timezone.now())
    f.save()
    for index, rowdata in enumerate(rows):
        item = Item(file=f, index=index)
        item.save()
        for d in rowdata:
            data = Data(item=item, description=d[0], value=d[1])
            data.save()
    return f
