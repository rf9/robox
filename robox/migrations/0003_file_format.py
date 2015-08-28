# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robox', '0002_auto_20150827_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='format',
            field=models.CharField(default='None', max_length=20),
            preserve_default=False,
        ),
    ]
