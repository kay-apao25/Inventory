# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0010_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='pr_num',
        ),
    ]