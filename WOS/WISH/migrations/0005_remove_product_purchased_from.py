# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0004_auto_20150420_0621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='purchased_from',
        ),
    ]
