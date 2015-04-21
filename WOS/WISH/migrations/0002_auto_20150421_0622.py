# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='garv',
            name='cc_num',
            field=models.ForeignKey(default=1, to='WISH.Cost_center'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='garv',
            name='confirmed_by',
            field=models.ForeignKey(related_name=b'dce_FK5', default=1, to='WISH.Employee'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='garv',
            name='date_confirmed',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='garv',
            name='date_inspected',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='garv',
            name='inspected_by',
            field=models.ForeignKey(related_name=b'dce_FK4', default=1, to='WISH.Employee'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='garv',
            name='noted_by',
            field=models.ForeignKey(related_name=b'dce_FK6', default=1, to='WISH.Employee'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='garv',
            name='par_num',
            field=models.ForeignKey(default=1, to='WISH.PAR'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='garv',
            name='qty',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='garv',
            name='remarks',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='garv',
            name='wo_num',
            field=models.ForeignKey(default=1, to='WISH.IRR'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='par',
            name='wo_num',
            field=models.ForeignKey(default=1, to='WISH.IRR'),
            preserve_default=False,
        ),
    ]
