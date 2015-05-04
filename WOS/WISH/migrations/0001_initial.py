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
                ('cost_center_name', models.TextField(max_length=20)),
                ('functional_group', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('credit_limit', models.FloatField()),
                ('debit_amount', models.FloatField()),
                ('credit_amount', models.FloatField()),
                ('balance_amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('dce', models.CharField(max_length=8, serialize=False, primary_key=True)),
                ('name', models.TextField()),
                ('charging_cc_no', models.CharField(max_length=20)),
                ('position', models.TextField()),
                ('cost_center_no', models.ForeignKey(to='WISH.Cost_center')),
            ],
        ),
        migrations.CreateModel(
            name='GARV',
            fields=[
                ('garv_date', models.DateField(null=True, blank=True)),
                ('garv_no', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('date_inspected', models.DateField(null=True, blank=True)),
                ('date_confirmed', models.DateField(null=True, blank=True)),
                ('cc_number', models.ForeignKey(blank=True, to='WISH.Cost_center', null=True)),
                ('confirmed_by', models.ForeignKey(related_name='dce_FK5', blank=True, to='WISH.Employee', null=True)),
                ('dce', models.ForeignKey(blank=True, to='WISH.Employee', null=True)),
                ('inspected_by', models.ForeignKey(related_name='dce_FK4', blank=True, to='WISH.Employee', null=True)),
                ('noted_by', models.ForeignKey(related_name='dce_FK6', blank=True, to='WISH.Employee', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory_stat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inv_station_no', models.CharField(max_length=20)),
                ('station_description', models.TextField()),
                ('cost_center_no', models.ForeignKey(to='WISH.Cost_center')),
            ],
        ),
        migrations.CreateModel(
            name='IRR',
            fields=[
                ('irr_no', models.IntegerField(serialize=False, primary_key=True)),
                ('date_recv', models.DateField(null=True, blank=True)),
                ('wo_no', models.CharField(max_length=7, null=True, blank=True)),
                ('remark', models.TextField(max_length=30, null=True, blank=True)),
                ('cost_center_no', models.ForeignKey(blank=True, to='WISH.Cost_center', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IRR_header',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reference', models.CharField(max_length=20)),
                ('invoice_number', models.CharField(max_length=20)),
                ('po_number', models.CharField(max_length=20)),
                ('dr_number', models.CharField(max_length=20)),
                ('proc_date', models.DateField()),
                ('approved_date', models.DateField()),
                ('type_n', models.CharField(max_length=20)),
                ('date_dlvrd', models.DateField()),
                ('dce_approved', models.ForeignKey(related_name='dce3', to='WISH.Employee')),
                ('dce_custodian', models.ForeignKey(related_name='dce1', to='WISH.Employee')),
                ('dce_user', models.ForeignKey(related_name='dce2', to='WISH.Employee')),
                ('inv_station_no', models.ForeignKey(to='WISH.Inventory_stat')),
            ],
        ),
        migrations.CreateModel(
            name='MIV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wrs_number', models.CharField(max_length=8)),
                ('date_issued', models.DateField()),
                ('doc_date', models.DateField()),
                ('remark', models.TextField()),
                ('inv_station_no', models.ForeignKey(to='WISH.Inventory_stat')),
                ('irr_no', models.ForeignKey(to='WISH.IRR')),
            ],
        ),
        migrations.CreateModel(
            name='PAR',
            fields=[
                ('par_date', models.DateField()),
                ('par_no', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('amt_cost', models.FloatField(null=True, blank=True)),
                ('remark', models.TextField(null=True, blank=True)),
                ('date_acquired', models.DateField(null=True, blank=True)),
                ('PO_number', models.ForeignKey(blank=True, to='WISH.IRR_header', null=True)),
                ('approved_by', models.ForeignKey(related_name='dce_FK2', blank=True, to='WISH.Employee', null=True)),
                ('dce', models.ForeignKey(blank=True, to='WISH.Employee', null=True)),
                ('inv_stat_no', models.ForeignKey(blank=True, to='WISH.Inventory_stat', null=True)),
                ('issued_by', models.ForeignKey(related_name='dce_FK3', blank=True, to='WISH.Employee', null=True)),
                ('wo_number', models.ForeignKey(blank=True, to='WISH.IRR', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pending',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_name', models.TextField()),
                ('serial_number', models.CharField(max_length=10)),
                ('model', models.TextField()),
                ('amount', models.FloatField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nsn', models.CharField(max_length=10)),
                ('slc_number', models.IntegerField()),
                ('product_number', models.CharField(max_length=10)),
                ('generic_name', models.TextField()),
                ('item_name', models.CharField(max_length=10)),
                ('brand', models.TextField()),
                ('part_number', models.CharField(max_length=8)),
                ('manufacture_date', models.DateField()),
                ('expiry_date', models.DateField(null=True, blank=True)),
                ('unit_cost', models.FloatField()),
                ('quantity', models.FloatField(default=b'1')),
                ('classification', models.CharField(max_length=30)),
                ('stock', models.CharField(max_length=10)),
                ('block', models.CharField(max_length=10)),
                ('unit_measure', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=10)),
                ('average_amount', models.FloatField()),
                ('balance_limit', models.FloatField()),
                ('serial_number', models.CharField(max_length=15)),
                ('model', models.TextField()),
                ('amount', models.FloatField()),
                ('description', models.TextField()),
                ('remark', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Product_to_GARV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qty', models.CharField(max_length=20)),
                ('remarks', models.CharField(max_length=20, null=True)),
                ('garv', models.ForeignKey(to='WISH.GARV')),
                ('par_number', models.ForeignKey(to='WISH.PAR')),
            ],
        ),
        migrations.CreateModel(
            name='Product_to_IRR',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity_accepted', models.FloatField()),
                ('quantity_rejected', models.FloatField()),
                ('quantity_balance', models.FloatField()),
                ('irr_no', models.ForeignKey(to='WISH.IRR')),
                ('product', models.ForeignKey(to='WISH.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Product_to_PAR',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qty', models.IntegerField()),
                ('par_no', models.ForeignKey(to='WISH.PAR')),
                ('product', models.ForeignKey(to='WISH.Product_to_IRR')),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('supplier_number', models.CharField(max_length=8)),
                ('supplier_name', models.TextField(max_length=20)),
                ('supplier_address', models.TextField(max_length=20)),
                ('telephone_number', models.CharField(max_length=20)),
                ('credit_limit', models.FloatField()),
                ('debit_amount', models.FloatField()),
                ('credit_amount', models.FloatField()),
                ('balance_amount', models.FloatField()),
                ('contact_person', models.TextField(max_length=20)),
                ('remarks', models.TextField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='product_to_garv',
            name='product',
            field=models.ForeignKey(to='WISH.Product_to_IRR'),
        ),
        migrations.AddField(
            model_name='product',
            name='purchased_from',
            field=models.ForeignKey(to='WISH.Supplier'),
        ),
        migrations.AddField(
            model_name='pending',
            name='supplier_number',
            field=models.ForeignKey(to='WISH.Supplier'),
        ),
        migrations.AddField(
            model_name='irr_header',
            name='supplier',
            field=models.ForeignKey(to='WISH.Supplier'),
        ),
        migrations.AddField(
            model_name='irr',
            name='irr_headkey',
            field=models.ForeignKey(to='WISH.IRR_header'),
        ),
        migrations.AddField(
            model_name='garv',
            name='wo_number',
            field=models.ForeignKey(blank=True, to='WISH.IRR_header', null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='dce',
            field=models.ForeignKey(to='WISH.Employee'),
        ),
        migrations.AlterUniqueTogether(
            name='pending',
            unique_together=set([('supplier_number', 'serial_number', 'model')]),
        ),
    ]
