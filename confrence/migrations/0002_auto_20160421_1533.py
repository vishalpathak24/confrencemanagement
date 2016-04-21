# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('confrence', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewr',
            name='confrence',
            field=models.ForeignKey(to='confrence.ConfrenceModel'),
        ),
        migrations.AlterField(
            model_name='reviewr',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
