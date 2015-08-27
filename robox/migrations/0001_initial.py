# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('value', models.DecimalField(max_digits=20, decimal_places=10)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='MetaData',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
                ('entry', models.ForeignKey(to='robox.Entry')),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='file',
            field=models.ForeignKey(to='robox.File'),
        ),
    ]
