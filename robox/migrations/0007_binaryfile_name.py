# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('robox', '0006_auto_20150917_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='binaryfile',
            name='name',
            field=models.CharField(max_length=64),
            preserve_default=False,
        ),
    ]
