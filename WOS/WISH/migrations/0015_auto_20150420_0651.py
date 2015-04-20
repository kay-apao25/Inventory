# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0014_auto_20150420_0650'),
    ]

    operations = [
        migrations.AddField(
            model_name='par',
            name='PO_num',
            field=models.ForeignKey(default=b'1', to='WISH.IRR_header'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='par',
            name='date_acquired',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='par',
            name='inv_stat_no',
            field=models.ForeignKey(default=b'1', to='WISH.Inventory_stat'),
            preserve_default=False,
        ),
    ]
