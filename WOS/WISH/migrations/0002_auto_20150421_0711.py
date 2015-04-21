# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='miv',
            name='asset_code_fk',
        ),
        migrations.RemoveField(
            model_name='miv',
            name='cost_center_no_fk',
        ),
        migrations.RemoveField(
            model_name='miv',
            name='inv_station_no_fk',
        ),
        migrations.RemoveField(
            model_name='miv',
            name='irr_no_fk',
        ),
        migrations.DeleteModel(
            name='MIV',
        ),
    ]
