# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0011_remove_product_pr_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pr_num',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
