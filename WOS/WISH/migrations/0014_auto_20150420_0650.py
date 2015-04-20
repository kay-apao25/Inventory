# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0013_irr_header_supl_fk'),
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
