# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('confrence', '0007_auto_20160424_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='confrencemodel',
            name='topics',
        ),
        migrations.AddField(
            model_name='topic',
            name='confrence',
            field=models.ForeignKey(to='confrence.ConfrenceModel', null=True),
        ),
    ]
