# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0008_remove_irr_header_date_dlvrd'),
    ]

    operations = [
        migrations.AddField(
            model_name='irr_header',
            name='date_dlvrd',
            field=models.DateField(default='2015-04-17'),
            preserve_default=False,
        ),
    ]
