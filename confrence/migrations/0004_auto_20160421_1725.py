# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('confrence', '0003_auto_20160421_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topicName', models.CharField(max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='Topics',
        ),
        migrations.AlterField(
            model_name='confrencemodel',
            name='topic',
            field=models.ManyToManyField(to='confrence.Topic'),
        ),
        migrations.AlterField(
            model_name='reviewr',
            name='topic',
            field=models.ForeignKey(to='confrence.Topic'),
        ),
    ]
