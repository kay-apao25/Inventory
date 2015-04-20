# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0003_product_pr_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='generic_name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='item_name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='model',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='remark',
            field=models.TextField(),
        ),
    ]
