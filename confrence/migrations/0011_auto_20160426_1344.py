# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 13:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('confrence', '0010_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, null=True)),
                ('status', models.CharField(max_length=30, null=True)),
                ('subFile', models.FileField(null=True, upload_to=b'files/')),
                ('upl_date', models.DateField(null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='confrence.Author')),
                ('confrence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confrence.Confrence')),
                ('topic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='confrence.Topic')),
            ],
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fl', models.FileField(upload_to=b'files/')),
                ('name', models.CharField(max_length=30)),
                ('upl_date', models.DateField()),
            ],
        ),
        migrations.RemoveField(
            model_name='reviewr',
            name='topic',
        ),
        migrations.AddField(
            model_name='reviewr',
            name='topics',
            field=models.ManyToManyField(to='confrence.Topic'),
        ),
        migrations.AddField(
            model_name='review',
            name='reviewr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confrence.Reviewr'),
        ),
        migrations.AddField(
            model_name='review',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confrence.Submission'),
        ),
    ]
