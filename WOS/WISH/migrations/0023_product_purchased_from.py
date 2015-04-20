# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0022_remove_product_purchased_from'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='purchased_from',
            field=models.ForeignKey(default=b'1', to='WISH.Supplier'),
            preserve_default=False,
        ),
    ]
