from django.db import models


# Create your models here.
class File(models.Model):
    upload_time = models.DateTimeField(auto_now_add=True)
    barcode = models.CharField(max_length=50)
    file = models.FileField(upload_to="data/")


class Entry(models.Model):
    file = models.ForeignKey(File)
    value = models.DecimalField(decimal_places=10, max_digits=20)


class MetaData(models.Model):
    entry = models.ForeignKey(Entry)
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
