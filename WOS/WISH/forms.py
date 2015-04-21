from django import forms

from .models import *

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('pr_num', 'inv_station_no_fk', 'cost_center_no_fk', 'item_name', \
        	'generic_name', 'brand', 'part_num', 'manufacture_date', 'expiry_date', 'class_n', 'stock', \
        	'stock', 'block', 'unit_measure', 'unit_cost', 'quantity', 'average_amt', 'status',\
        	'balance_limit', 'serial_number', 'model', 'amount', 'description', 'remark', 'purchased_from',)

class IRR_entryForm(forms.ModelForm):

    class Meta:
        model = IRR_header
        fields = ('irr_headkey', 'inv_station_no', 'reference', 'invoice_num', 'po_num', 'dr_num', \
        	'dce_custodian', 'dce_user', 'proc_date', 'type_n', 'remark', 'date_dlvrd', 'supl_fk',)

class IRR_entry_cont_Form(forms.ModelForm):

    class Meta:
        model = IRR
        fields = ('irr_no_fk', 'asset_code_fk', 'cost_center_no_fk' ,'quantity_actual', \
    'quantity_accepted' ,'quantity_rejected' , 'quantity_balance' , 'date_recv' , 'wo_no' , 'remark',)

class MIV_entryForm(forms.ModelForm):

    class Meta:
    	model = MIV
    	fields = ( 'irr_no_fk', 'inv_station_no_fk', 'asset_code_fk' , 'dce_custodian_fk', 'dce_user_fk' , \
    		'cost_center_no_fk' ,  'quantity' , 'amount', 'date_issued',  'doc_date' , 'remark' )

class PAR_entryForm(forms.ModelForm):

    class Meta:
        model = PAR
        fields = ('dce_FK', 'asset_code_FK', 'par_date', 'par_no', 'amt_cost', 'remark', 'qty', 'approved_by', \
        'issued_by', 'inv_stat_no', 'PO_num', 'date_acquired',)
