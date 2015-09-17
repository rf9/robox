# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    replaces = [('robox', '0001_initial'), ('robox', '0002_auto_20150827_1328'), ('robox', '0003_file_format'),
                ('robox', '0004_remove_entry_value'), ('robox', '0005_auto_20150907_1601'),
                ('robox', '0006_auto_20150917_1025'), ('robox', '0007_binaryfile_name')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BinaryFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('data', models.BinaryField()),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('barcode', models.CharField(default='', max_length=50)),
                ('binary_file', models.ForeignKey(to='robox.BinaryFile')),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('format', models.CharField(default='None', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('data_file', models.ForeignKey(to='robox.DataFile')),
            ],
        ),
        migrations.CreateModel(
            name='MetaData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('key', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
                ('entry', models.ForeignKey(to='robox.Entry')),
            ],
        ),
    ]
