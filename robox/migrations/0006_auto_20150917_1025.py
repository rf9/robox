# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('robox', '0005_auto_20150907_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='BinaryFile',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('data', models.BinaryField()),
            ],
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.ForeignKey(to='robox.BinaryFile'),
        ),
    ]
