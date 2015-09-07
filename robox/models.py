from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.utils.datastructures import OrderedSet
from django.utils.functional import cached_property


class File(models.Model):
    upload_time = models.DateTimeField(auto_now_add=True)
    barcode = models.CharField(max_length=50)
    file = models.FileField(upload_to="data/")
    format = models.CharField(max_length=20)

    @cached_property
    def headings(self):
        headings = OrderedSet()
        for entry in self.entry_set.all():
            for meta_data in entry.metadata_set.all():
                headings.add(meta_data.key)
        return headings

    def content(self):
        entry_data = []
        for entry in self.entry_set.all():
            data = {meta_data.key: meta_data.value for meta_data in entry.metadata_set.all()}
            entry_data.append([data[heading] for heading in self.headings])
        return entry_data

    def recent(self):
        return self.upload_time > timezone.now() - timedelta(seconds=30)


class Entry(models.Model):
    file = models.ForeignKey(File)


class MetaData(models.Model):
    entry = models.ForeignKey(Entry)
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
