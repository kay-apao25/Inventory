# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0002_auto_20150420_0619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='par',
            name='PO_num',
        ),
        migrations.RemoveField(
            model_name='par',
            name='date_acquired',
        ),
        migrations.RemoveField(
            model_name='par',
            name='inv_stat_no',
        ),
    ]
