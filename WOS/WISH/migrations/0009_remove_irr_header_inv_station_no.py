# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0008_product_purchased_from'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='irr_header',
            name='inv_station_no',
        ),
    ]
