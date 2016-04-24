# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('confrence', '0002_auto_20160421_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topicName', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='reviewr',
            name='topic',
            field=models.CharField(default=b'hola', max_length=30),
        ),
        migrations.AddField(
            model_name='confrencemodel',
            name='topic',
            field=models.ManyToManyField(to='confrence.Topics'),
        ),
    ]
