# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0002_auto_20150421_0622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='miv',
            name='cost_center_no_fk',
        ),
        migrations.RemoveField(
            model_name='miv',
            name='dce_custodian_fk',
        ),
        migrations.RemoveField(
            model_name='miv',
            name='dce_user_fk',
        ),
    ]
