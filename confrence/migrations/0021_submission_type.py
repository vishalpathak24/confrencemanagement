# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('confrence', '0020_auto_20160426_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='type',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
