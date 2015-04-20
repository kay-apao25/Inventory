# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0012_auto_20150420_0627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='irr_header',
            name='supl_fk',
        ),
    ]
