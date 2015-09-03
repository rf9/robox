from django.db import models


class File(models.Model):
    upload_time = models.DateTimeField(auto_now_add=True)
    barcode = models.CharField(max_length=50)
    file = models.FileField(upload_to="data/")
    format = models.CharField(max_length=20)


class Entry(models.Model):
    file = models.ForeignKey(File)


class MetaData(models.Model):
    entry = models.ForeignKey(Entry)
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
