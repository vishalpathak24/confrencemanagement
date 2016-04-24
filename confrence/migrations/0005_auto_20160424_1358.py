# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('confrence', '0004_auto_20160421_1725'),
    ]

    operations = [
        migrations.RenameField(
            model_name='confrencemodel',
            old_name='oraganiser',
            new_name='oraganizer',
        ),
    ]
