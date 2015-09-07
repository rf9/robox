from collections import defaultdict, namedtuple
from django.db import models
from django.utils.datastructures import OrderedSet

STR_MAX = 64

IndexedTableRow = namedtuple('IndexedTableRow', 'index elements')

class File(models.Model):
    barcode = models.CharField(max_length=STR_MAX)
    filename = models.CharField(max_length=STR_MAX)
    upload_date = models.DateTimeField()

    def __str__(self):
        return self.filename

    def headings(self):
        items = self.item_set.all()
        headings = OrderedSet()
        for item in items:
            data = item.data_set.all()
            for d in data:
                headings.add(d.description)
        return list(headings)

    def table_content(self, headings):
        items = self.item_set.all()
        tabledata = []
        for item in items:
            data = item.data_set.all()
            rowdata = defaultdict(list)
            for d in data:
                rowdata[d.description].append(d.value)
            tablerow = IndexedTableRow(item.index, [','.join(rowdata[h]) for h in headings])
            tabledata.append(tablerow)
        return tabledata


class Item(models.Model):
    file = models.ForeignKey(File)
    index = models.IntegerField()

    def __str__(self):
        return '%s[%s]' % (self.file, self.index)


class Data(models.Model):
    item = models.ForeignKey(Item)
    description = models.CharField(max_length=STR_MAX)
    value = models.CharField(max_length=STR_MAX)

    def __str__(self):
        return '%s:%s' % (self.description, self.value)
