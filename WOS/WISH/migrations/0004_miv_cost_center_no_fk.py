# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0003_auto_20150421_0651'),
    ]

    operations = [
        migrations.AddField(
            model_name='miv',
            name='cost_center_no_fk',
            field=models.ForeignKey(default=1, to='WISH.Cost_center'),
            preserve_default=False,
        ),
    ]
