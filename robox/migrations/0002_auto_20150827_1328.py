# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):
    dependencies = [
        ('robox', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='barcode',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='file',
            field=models.FileField(default='', upload_to='data/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='upload_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 27, 13, 28, 11, 611856, tzinfo=utc),
                                       auto_now_add=True),
            preserve_default=False,
        ),
    ]
