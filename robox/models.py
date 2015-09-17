from datetime import timedelta
import logging

from django.db import models
from django.db.transaction import atomic
from django.utils import timezone
from django.utils.datastructures import OrderedSet
from django.utils.functional import cached_property

from robox import parsing

_logger = logging.getLogger(__name__)


class File(models.Model):
    upload_time = models.DateTimeField(auto_now_add=True)
    barcode = models.CharField(max_length=50)
    file = models.ForeignKey('BinaryFile')
    format = models.CharField(max_length=20, default="None")

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

    @atomic
    def parse(self):
        # Delete any old entries (in case it is a reparse.
        Entry.objects.filter(file=self).delete()

        try:
            _logger.debug(self.file.data)
            parsed_file = parsing.parse(self.file.data)
        except parsing.RoboxParsingError as err:
            _logger.info("Unparsed file %s" % self.file.name)
        else:
            self.format = parsed_file['parser']
            self.save()

            _logger.debug("File parsed: %s as %s" % (self.file.name, self.format))

            for data in parsed_file['data']:
                entry = Entry.objects.create(file=self)
                for key, value in data.items():
                    MetaData.objects.create(entry=entry, key=key, value=value)


class BinaryFile(models.Model):
    name = models.CharField(max_length=64)
    data = models.BinaryField()

    def __str__(self):
        return self.name


class Entry(models.Model):
    file = models.ForeignKey(File)


class MetaData(models.Model):
    entry = models.ForeignKey(Entry)
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
