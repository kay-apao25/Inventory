# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0018_remove_par_issued_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='par',
            name='issued_by',
            field=models.ForeignKey(related_name=b'dce_FK3', default=b'1', to='WISH.Employee'),
            preserve_default=False,
        ),
    ]
