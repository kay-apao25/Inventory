# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0013_remove_irr_header_supl_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='irr_header',
            name='supl_fk',
            field=models.ForeignKey(default=1, to='WISH.Supplier'),
            preserve_default=False,
        ),
    ]
