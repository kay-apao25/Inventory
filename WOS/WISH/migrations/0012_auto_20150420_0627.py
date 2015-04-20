# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0011_auto_20150420_0627'),
    ]

    operations = [
        migrations.AddField(
            model_name='irr_header',
            name='date_dlvrd',
            field=models.DateField(default=1984),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='irr_header',
            name='supl_fk',
            field=models.ForeignKey(default=1, to='WISH.Supplier'),
            preserve_default=False,
        ),
    ]
