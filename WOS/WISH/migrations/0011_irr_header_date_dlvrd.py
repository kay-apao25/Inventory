# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0010_remove_irr_header_date_dlvrd'),
    ]

    operations = [
        migrations.AddField(
            model_name='irr_header',
            name='date_dlvrd',
            field=models.DateField(default=datetime.datetime(2015, 4, 20, 6, 32, 54, 979751, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
