from django import forms

from .models import *

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('nsn', 'pr_num', 'slc_num', 'inv_station_no_fk', 'cost_center_no_fk', 'item_name', \
        	'generic_name', 'brand', 'part_num', 'manufacture_date', 'expiry_date', 'class_n', 'stock', \
        	'stock', 'block', 'unit_measure', 'unit_cost', 'quantity', 'average_amt', 'status',\
        	'balance_limit', 'serial_number', 'model', 'amount', 'description', 'remark', 'purchased_from',)

class IRR_entryForm(forms.ModelForm):

    class Meta:
        model = IRR_header
        fields = ('irr_headkey', 'inv_station_no', 'reference', 'invoice_num', 'po_num', 'dr_num', \
        	'dce_custodian', 'dce_user', 'proc_date', 'type_n', 'remark', 'date_dlvrd', 'supl_fk',)

