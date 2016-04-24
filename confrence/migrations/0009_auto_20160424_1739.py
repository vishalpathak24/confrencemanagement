# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('confrence', '0008_auto_20160424_1718'),
    ]

    operations = [
        migrations.CreateModel(
            name='Confrence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('confrenceName', models.CharField(max_length=30)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='confrencemodel',
            name='organizer',
        ),
        migrations.AlterField(
            model_name='reviewr',
            name='confrence',
            field=models.ForeignKey(to='confrence.Confrence'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='confrence',
            field=models.ForeignKey(to='confrence.Confrence', null=True),
        ),
        migrations.DeleteModel(
            name='ConfrenceModel',
        ),
    ]
