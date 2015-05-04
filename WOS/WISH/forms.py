from django import forms
from .models import *

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('product_number', 'item_name', \
        	'generic_name', 'brand', 'part_number', 'manufacture_date', 'expiry_date', 'classification', \
        	'stock', 'block', 'unit_measure', 'unit_cost', 'quantity', 'average_amount', 'status',\
        	'balance_limit', 'serial_number', 'model', 'description', 'remark', 'purchased_from',)

class IRR_entryForm(forms.ModelForm):

    class Meta:
        model = IRR_header
        fields = ( 'inv_station_no', 'supplier', 'reference', 'invoice_number', 'po_number', 'dr_number', \
            'dce_custodian', 'dce_user', 'dce_approved','proc_date', 'approved_date','type_n', 'date_dlvrd',)

class IRR_entry_cont_Form(forms.ModelForm):

    class Meta:
        model = IRR
        fields = ('cost_center_no', 'date_recv' , 'wo_no' , 'remark',)

class Product_to_IRRForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity_accepted = forms.FloatField()
    quantity_rejected = forms.FloatField()
    quantity_balance = forms.FloatField()
    
class MIV_entryForm(forms.ModelForm):

    class Meta:
        model = MIV
        fields = ( 'date_issued', 'inv_station_no', 'remark')
        '''widgets = {
            'quantity': forms.TextInput(attrs={'placeholder': 'Quantity'}),
            'date_issued': forms.TextInput(attrs={'placeholder': 'Date Issued'}),
            'remark': forms.TextInput(attrs={'placeholder': 'Remark'}),
            #'asset_code': forms.TextInput(attrs={'placeholder': 'Asset Code'}),
            'irr_no': forms.TextInput(attrs={'placeholder': 'IRR No.'}),
            'inv_station_no': forms.TextInput(attrs={'placeholder': 'Inventory Station No.'}),
        }
        fields = ( 'quantity', 'date_issued',  'remark' , 'product', 'inv_station_no',)'''

class PAR_entryForm(forms.ModelForm):

    class Meta:
        model = PAR
        fields = ('dce', 'par_no', 'amt_cost', 'approved_by', \
        'issued_by', 'inv_stat_no', 'PO_number', 'date_acquired', 'wo_number', 'remark', )

class PAR_Form(forms.ModelForm):

    class Meta:
        model = PAR
        fields = ('dce', 'amt_cost', 'approved_by', \
        'issued_by', 'inv_stat_no', 'PO_number', 'date_acquired', 'wo_number', 'remark',)

class Product_to_PARForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset = Product_to_IRR.objects.all() )

    class Meta:
        model = Product_to_PAR
        fields = ('product', 'qty', )

class GARV_entryForm(forms.ModelForm):

    class Meta:
        model = GARV
        fields = ('dce', 'garv_no', 'cc_number', 'wo_number',\
                    'inspected_by', 'date_inspected', 'confirmed_by', \
                    'date_confirmed', 'noted_by', )

class Product_to_GARVform(forms.ModelForm):

    class Meta:
        model = Product_to_GARV
        fields = ('product', 'qty', 'par_number', 'remarks',)

class TryForm(forms.ModelForm):

    class Meta:
        model = Try
        fields = ('text',)

