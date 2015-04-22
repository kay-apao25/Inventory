# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0004_auto_20150421_0810'),
    ]

    operations = [
        migrations.CreateModel(
            name='MIV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wrs_num', models.CharField(max_length=8)),
                ('quantity', models.FloatField()),
                ('amount', models.FloatField()),
                ('date_issued', models.DateField(null=True, blank=True)),
                ('doc_date', models.DateField(null=True, blank=True)),
                ('remark', models.TextField()),
                ('asset_code_fk', models.ForeignKey(to='WISH.Product')),
                ('cost_center_no_fk', models.ForeignKey(to='WISH.Cost_center')),
                ('inv_station_no_fk', models.ForeignKey(to='WISH.Inventory_stat')),
                ('irr_no_fk', models.ForeignKey(to='WISH.IRR_header')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
