# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0007_irr_header_inv_station_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='irr_header',
            name='inv_station_no',
        ),
    ]
