# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robox', '0004_remove_entry_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='format',
            field=models.CharField(default='None', max_length=20),
        ),
    ]
