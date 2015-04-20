# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0004_auto_20150420_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='irr_header',
            name='date_dlvrd',
            field=models.DateField(default=0),
            preserve_default=False,
        ),
    ]
