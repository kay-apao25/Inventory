# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0002_remove_par_inv_stat_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='par',
            name='inv_stat_no',
            field=models.ForeignKey(default=b'1', to='WISH.Inventory_stat'),
            preserve_default=False,
        ),
    ]
