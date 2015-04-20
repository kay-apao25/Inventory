# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0015_auto_20150420_0651'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='par',
            name='approved_by',
        ),
    ]
