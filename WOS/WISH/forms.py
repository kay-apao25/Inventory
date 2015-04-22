from django import forms

from .models import *

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('product_number', 'inv_station_no', 'cost_center_no', 'item_name', \
        	'generic_name', 'brand', 'part_number', 'manufacture_date', 'expiry_date', 'classification', 'stock', \
        	'stock', 'block', 'unit_measure', 'unit_cost', 'quantity', 'average_amount', 'status',\
        	'balance_limit', 'serial_number', 'model', 'description', 'remark', 'purchased_from',)

class IRR_entryForm(forms.ModelForm):

    class Meta:
        model = IRR_header
        fields = ( 'inv_station_no', 'supplier', 'reference', 'invoice_number', 'po_number', 'dr_number', \
            'dce_custodian', 'dce_user', 'proc_date', 'type_n', 'remark', 'date_dlvrd',)

class IRR_entry_cont_Form(forms.ModelForm):

    class Meta:
        model = IRR
        fields = ('cost_center_no' ,'quantity_actual', 'asset_code',\
    'quantity_accepted', 'date_recv' , 'wo_no' , 'remark',)

class MIV_entryForm(forms.ModelForm):

    class Meta:
        model = MIV
        fields = ( 'quantity', 'date_issued',  'remark' , 'asset_code_fk', 'irr_no_fk', 'inv_station_no_fk', 'cost_center_no_fk',)

class WRSForm(forms.Form):
    wrs_num = forms.IntegerField(
        label="Enter WRS number",
        required=True,
    )

class PAR_entryForm(forms.ModelForm):

    class Meta:
        model = PAR
        fields = ('dce', 'asset_code', 'par_no', 'amt_cost', 'remark', 'qty', 'approved_by', \
        'issued_by', 'inv_stat_no', 'PO_number', 'date_acquired', 'wo_number', )

class GARV_entryForm(forms.ModelForm):

    class Meta:
        model = GARV
        fields = ('dce', 'asset_code', 'garv_no', 'cc_number', 'wo_number', 'qty',\
                    'par_number', 'remarks', 'inspected_by', 'date_inspected', 'confirmed_by', \
                    'date_confirmed', 'noted_by', )
