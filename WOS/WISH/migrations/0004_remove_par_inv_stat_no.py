# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0003_par_inv_stat_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='par',
            name='inv_stat_no',
        ),
    ]
