# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0009_remove_irr_header_inv_station_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='irr_header',
            name='inv_station_no',
            field=models.ForeignKey(default=1, to='WISH.Inventory_stat'),
            preserve_default=False,
        ),
    ]
