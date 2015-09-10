# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robox', '0003_file_format'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='value',
        ),
    ]
