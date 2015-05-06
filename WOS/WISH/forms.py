from django import forms
from .forms import *
from .views import *

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('product_number', 'item_name', 'nsn',\
            'generic_name', 'brand', 'part_number', 'manufacture_date', 'expiry_date', 'classification', \
            'stock', 'block', 'unit_measure', 'unit_cost', 'quantity', 'average_amount', 'status', \
            'balance_limit', 'serial_number', 'model', 'description', 'remark', 'purchased_from', 'inv_station_no',)

class ProductForm1(forms.Form):
    nsn = forms.CharField(max_length=10)
    slc_number = forms.CharField(max_length=10)
    product_number = forms.CharField(max_length=10)
    generic_name = forms.CharField(max_length=25)
    item_name = forms.CharField(max_length=10)
    brand = forms.CharField(max_length=25)
    part_number = forms.CharField(max_length=8)
    manufacture_date = forms.DateField()
    inv_station_no = forms.ModelChoiceField(queryset=Inventory_stat.objects.all())

class ProductForm2(forms.Form):
    expiry_date = forms.DateField()
    unit_cost = forms.FloatField()
    quantity = forms.FloatField()
    classification = forms.CharField(max_length=30)
    stock = forms.CharField(max_length=10)
    block = forms.CharField(max_length=10)
    unit_measure = forms.CharField(max_length=10)
    status = forms.CharField(max_length=10)

class ProductForm3(forms.Form):
    purchased_from = forms.ModelChoiceField(queryset=Supplier.objects.all())
    average_amount = forms.FloatField()
    balance_limit = forms.FloatField()
    serial_number = forms.CharField(max_length=15)
    model = forms.CharField(max_length=25)
    amount = forms.FloatField()
    description = forms.CharField(max_length=25)
    remark = forms.CharField(max_length=25)


class IRR_entryForm(forms.ModelForm):
    class Meta:
        model = IRR_header
        exclude = ('inv_station_no', 'supplier', 'reference', 'invoice_number', 'po_number', 'dr_number',\
                    'dce_custodian', 'dce_user', 'dce_approved','proc_date', 'approved_date','type_n', 'date_dlvrd',)


class IRR_entryForm1(forms.Form):
    inv_station_no = forms.ModelChoiceField(queryset=Inventory_stat.objects.all())
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all())
    reference = forms.CharField()
    invoice_number = forms.CharField()
    po_number = forms.CharField()
    dr_number = forms.CharField()


class IRR_entryForm2(forms.Form):
    dce_custodian = forms.ModelChoiceField(queryset=Employee.objects.all())
    dce_user = forms.ModelChoiceField(queryset=Employee.objects.all())
    dce_approved = forms.ModelChoiceField(queryset=Employee.objects.all())
    proc_date = forms.DateField()
    approved_date = forms.DateField()
    type_n = forms.CharField()
    date_dlvrd = forms.DateField()

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
        fields = ( 'date_issued', 'remark')
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
        fields = ('dce', 'par_no', 'approved_by', \
        'issued_by', 'PO_number', 'date_acquired', 'remark', )

class PAR_Form(forms.ModelForm):

    class Meta:
        model = PAR
        fields = ('dce', 'approved_by', \
        'issued_by', 'PO_number', 'date_acquired', 'remark',)


class Product_to_PARForm(forms.Form):
    product = forms.ModelChoiceField(Product.objects.all())
    qty = forms.IntegerField()


class GARV_entryForm(forms.ModelForm):

    class Meta:
        model = GARV
        fields = ('garv_no', 'cc_number', \
                    'inspected_by', 'date_inspected', 'confirmed_by', \
                    'date_confirmed', 'noted_by', )

class GARV_Form(forms.ModelForm):

    class Meta:
        model = GARV
        fields = ('cc_number', \
                    'inspected_by', 'date_inspected', 'confirmed_by', \
                    'date_confirmed', 'noted_by', )

class Product_to_GARVform(forms.Form):

    product = forms.ModelChoiceField(queryset=Product.objects.all())
    qty = forms.FloatField()
    remarks = forms.CharField()


class Product_to_GARVform1(forms.Form):

    product = forms.ModelChoiceField(queryset=Product.objects.all())
    qty = forms.FloatField()
    remarks = forms.CharField()
