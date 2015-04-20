# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WISH', '0004_auto_20150420_0000'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('credit_limit', models.FloatField()),
                ('debit_amt', models.FloatField()),
                ('credit_amt', models.FloatField()),
                ('balance_amt', models.FloatField()),
                ('dce_fk', models.ForeignKey(to='WISH.Employee')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
