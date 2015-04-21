from django import forms

from .models import *

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('pr_num', 'inv_station_no_fk', 'cost_center_no_fk', 'item_name', \
        	'generic_name', 'brand', 'part_num', 'manufacture_date', 'expiry_date', 'class_n', 'stock', \
        	'stock', 'block', 'unit_measure', 'unit_cost', 'quantity', 'average_amt', 'status',\
        	'balance_limit', 'serial_number', 'model', 'description', 'remark', 'purchased_from',)

class IRR_entryForm(forms.ModelForm):

    class Meta:
        model = IRR_header
        fields = ('irr_headkey', 'reference', 'invoice_num', 'po_num', 'dr_num', \
        	'dce_custodian', 'dce_user', 'proc_date', 'type_n', 'remark', 'date_dlvrd',)

class IRR_entry_cont_Form(forms.ModelForm):

    class Meta:
        model = IRR
        fields = ('cost_center_no_fk' ,'quantity_actual', \
    'quantity_accepted', 'date_recv' , 'wo_no' , 'remark',)

class MIV_entryForm(forms.ModelForm):

    class Meta:
    	model = MIV
    	fields = ( 'irr_no_fk', 'inv_station_no_fk', 'asset_code_fk' , 'dce_custodian_fk', 'dce_user_fk' , \
    		'cost_center_no_fk' , 'wrs_num' ,  'quantity', 'date_issued',  'remark' ,)

class PAR_entryForm(forms.ModelForm):

    class Meta:
        model = PAR
        fields = ('dce_FK', 'asset_code_FK', 'par_no', 'amt_cost', 'remark', 'qty', 'approved_by', \
        'issued_by', 'inv_stat_no', 'PO_num', 'date_acquired',)
