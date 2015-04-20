# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0005_par_inv_stat_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='irr_header',
            name='inv_station_no',
        ),
    ]
