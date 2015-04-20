# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cost_center',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cost_center_name', models.TextField(max_length=50)),
                ('functional_group', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('dce', models.CharField(max_length=8, serialize=False, primary_key=True)),
                ('name', models.TextField()),
                ('charging_cc_no', models.CharField(max_length=20)),
                ('position', models.TextField()),
                ('cost_center_no_fk', models.ForeignKey(to='WISH.Cost_center')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GARV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('garv_date', models.DateField(null=True, blank=True)),
                ('garv_no', models.CharField(max_length=50, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Inventory_stat',
            fields=[
                ('inv_station_no', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('station_description', models.TextField()),
                ('cost_center_no_fk', models.ForeignKey(to='WISH.Cost_center')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IRR_header',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('irr_headkey', models.CharField(max_length=30)),
                ('inv_station_no', models.CharField(max_length=20)),
                ('reference', models.CharField(max_length=20)),
                ('invoice_num', models.CharField(max_length=20)),
                ('po_num', models.CharField(max_length=20)),
                ('dr_num', models.CharField(max_length=20)),
                ('proc_date', models.DateField()),
                ('type_n', models.CharField(max_length=20)),
                ('remark', models.TextField(max_length=100)),
                ('dce_custodian', models.ForeignKey(related_name='dce1', to='WISH.Employee')),
                ('dce_user', models.ForeignKey(related_name='dce2', to='WISH.Employee')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PAR',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('par_date', models.DateField(null=True, blank=True)),
                ('par_no', models.CharField(max_length=50, null=True)),
                ('amt_cost', models.FloatField()),
                ('remark', models.TextField()),
                ('qty', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pending',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_name', models.TextField()),
                ('serial_number', models.CharField(max_length=50)),
                ('model', models.TextField()),
                ('amount', models.FloatField()),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nsn', models.CharField(max_length=10)),
                ('slc_num', models.IntegerField()),
                ('item_name', models.TextField(max_length=80)),
                ('generic_name', models.TextField(max_length=100)),
                ('brand', models.TextField(max_length=50)),
                ('part_num', models.CharField(max_length=8)),
                ('manufacture_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('class_n', models.CharField(max_length=30)),
                ('stock', models.CharField(max_length=20)),
                ('block', models.CharField(max_length=20)),
                ('unit_measure', models.CharField(max_length=20)),
                ('unit_cost', models.FloatField()),
                ('quantity', models.FloatField()),
                ('average_amt', models.FloatField()),
                ('status', models.CharField(max_length=20)),
                ('balance_limit', models.FloatField()),
                ('serial_number', models.CharField(max_length=30)),
                ('model', models.TextField(max_length=50)),
                ('amount', models.FloatField()),
                ('description', models.TextField(max_length=50)),
                ('remark', models.TextField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IRR',
            fields=[
                ('asset_code_fk', models.ForeignKey(primary_key=True, serialize=False, to='WISH.Product')),
                ('quantity_actual', models.FloatField()),
                ('quantity_accepted', models.FloatField()),
                ('quantity_rejected', models.FloatField()),
                ('quantity_balance', models.FloatField()),
                ('date_recv', models.DateField(null=True, blank=True)),
                ('wo_no', models.CharField(max_length=7)),
                ('remark', models.TextField()),
                ('cost_center_no_fk', models.ForeignKey(to='WISH.Cost_center')),
                ('irr_no_fk', models.ForeignKey(to='WISH.IRR_header')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('supplier_num', models.CharField(max_length=8)),
                ('supplier_name', models.TextField(max_length=50)),
                ('supplier_address', models.TextField(max_length=50)),
                ('telephone_number', models.CharField(max_length=20)),
                ('credit_limit', models.FloatField()),
                ('debit_amt', models.FloatField()),
                ('credit_amt', models.FloatField()),
                ('balance_amt', models.FloatField()),
                ('contact_person', models.TextField(max_length=50)),
                ('remarks', models.TextField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='cost_center_no_fk',
            field=models.ForeignKey(to='WISH.Cost_center'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='inv_station_no_fk',
            field=models.ForeignKey(to='WISH.Inventory_stat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pending',
            name='supplier_num',
            field=models.ForeignKey(to='WISH.Supplier'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='pending',
            unique_together=set([('supplier_num', 'serial_number', 'model')]),
        ),
        migrations.AddField(
            model_name='par',
            name='asset_code_FK',
            field=models.ForeignKey(to='WISH.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='par',
            name='dce_FK',
            field=models.ForeignKey(to='WISH.Employee'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='par',
            unique_together=set([('dce_FK', 'asset_code_FK')]),
        ),
        migrations.AddField(
            model_name='miv',
            name='asset_code_fk',
            field=models.ForeignKey(to='WISH.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='miv',
            name='cost_center_no_fk',
            field=models.ForeignKey(to='WISH.Cost_center'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='miv',
            name='dce_custodian_fk',
            field=models.ForeignKey(related_name='dce3', to='WISH.Employee'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='miv',
            name='dce_user_fk',
            field=models.ForeignKey(related_name='dce4', to='WISH.Employee'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='miv',
            name='inv_station_no_fk',
            field=models.ForeignKey(to='WISH.Inventory_stat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='miv',
            name='irr_no_fk',
            field=models.ForeignKey(to='WISH.IRR_header'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='garv',
            name='asset_code_FK',
            field=models.ForeignKey(to='WISH.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='garv',
            name='dce_FK',
            field=models.ForeignKey(to='WISH.Employee'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='garv',
            unique_together=set([('dce_FK', 'asset_code_FK')]),
        ),
    ]
