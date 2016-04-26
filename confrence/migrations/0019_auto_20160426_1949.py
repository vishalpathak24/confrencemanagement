# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('confrence', '0018_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='papersubmission',
            name='filesize',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='postersubmission',
            name='filesize',
            field=models.IntegerField(),
        ),
    ]
