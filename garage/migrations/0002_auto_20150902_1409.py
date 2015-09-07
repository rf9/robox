# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('description', models.CharField(max_length=64)),
                ('value', models.CharField(max_length=64)),
                ('item', models.ForeignKey(to='garage.Item')),
            ],
        ),
        migrations.RemoveField(
            model_name='metadata',
            name='item',
        ),
        migrations.AddField(
            model_name='file',
            name='barcode',
            field=models.CharField(default=datetime.datetime(2015, 9, 2, 14, 9, 50, 138440, tzinfo=utc), max_length=64),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Metadata',
        ),
    ]
