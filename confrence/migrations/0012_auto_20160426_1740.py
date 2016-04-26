# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('confrence', '0011_auto_20160426_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='reviewed',
            field=models.BooleanField(default=False),
        ),
    ]
