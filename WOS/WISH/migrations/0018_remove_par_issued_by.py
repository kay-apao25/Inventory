# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0017_par_approved_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='par',
            name='issued_by',
        ),
    ]
