# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('confrence', '0005_auto_20160424_1358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='confrencemodel',
            old_name='oraganizer',
            new_name='organizer',
        ),
    ]
