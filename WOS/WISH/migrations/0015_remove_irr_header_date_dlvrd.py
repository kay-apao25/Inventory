# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0014_irr_header_supl_fk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='irr_header',
            name='date_dlvrd',
        ),
    ]
