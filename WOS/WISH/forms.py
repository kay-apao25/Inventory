from django import forms
from .forms import *
from .views import *
from django.db.models import Q

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('product_number', 'item_name', 'nsn', 'generic_name', 'brand',\
            'part_number', 'manufacture_date', 'expiry_date', 'classification', \
            'stock', 'block', 'unit_measure', 'unit_cost', 'quantity', \
            'average_amount', 'status', 'balance_limit', 'serial_number',\
            'model', 'description', 'remarks', 'purchased_from', 'inv_station_no', \
            'slc_number', 'amount', )

    class ProductForm1(forms.Form):
        nsn = forms.CharField(label='NSN *', max_length=10)
        product_number = forms.CharField(label='Product number *', max_length=10)
        generic_name = forms.CharField(label='Generic name *', max_length=25)
        item_name = forms.CharField(label='Item name*', max_length=10)
        brand = forms.CharField(label='Brand *', max_length=25)
        part_number = forms.CharField(label='Part number *', max_length=8)
        manufacture_date = forms.DateField(label='Manufacture date *', widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
        inv_station_no = forms.ModelChoiceField(label='Inventory station *', queryset=Inventory_stat.objects.all())

    class ProductForm2(forms.Form):
        UNIT_CHOICES = (
            ('unit', 'unit'),
            ('piece', 'piece'),
            ('box', 'box'),
            ('pack', 'pack'),
            ('pad', 'pad'),
            ('ream', 'ream'),
        )
        expiry_date = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}), required=False)
        unit_cost = forms.DecimalField(label='Unit cost*', decimal_places=2)
        quantity = forms.IntegerField(initial='1', label='Quantity *')
        classification = forms.CharField(label='Classification*', max_length=30)
        stock = forms.CharField(label='Stock *', max_length=10)
        block = forms.CharField(label='Block *', max_length=10)
        unit_measure = forms.ChoiceField(label='Unit measure *', choices=UNIT_CHOICES)
        status = forms.CharField(label='Status *', max_length=10, initial='Pending')

    class ProductForm3(forms.Form):
        purchased_from = forms.ModelChoiceField(queryset=Supplier.objects.all(), label='Purchased from *')
        average_amount = forms.FloatField(label='Average amount *')
        balance_limit = forms.FloatField(label='Balance limit *')
        serial_number = forms.CharField(max_length=15, required=False)
        model = forms.CharField(label='Model *', max_length=25)
        description = forms.CharField(label='Description*', max_length=25)
        remarks = forms.CharField(max_length=25, required=False)

class ProductForm5(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('product_number', 'item_name', 'nsn', 'generic_name', 'brand',\
            'part_number', 'manufacture_date', 'expiry_date', 'classification', \
            'stock', 'block', 'unit_measure', 'unit_cost', 'quantity', \
            'average_amount', 'status', 'balance_limit', 'serial_number',\
            'model', 'description', 'remarks', 'purchased_from', 'inv_station_no', \
            'slc_number', 'amount', )

class IRR_entryForm(forms.ModelForm):
    class Meta:
        model = IRR_header
        exclude = ('inv_station_no', 'supplier', 'reference', 'invoice_number', 'po_number', 'dr_number',\
                    'dce_custodian', 'dce_user', 'dce_approved','proc_date', 'approved_date','type_n', 'date_dlvrd',)


class IRR_entryForm1(forms.Form):
    inv_station_no = forms.ModelChoiceField(label='Inventory station *', queryset=Inventory_stat.objects.all())
    supplier = forms.ModelChoiceField(label='Supplier *', queryset=Supplier.objects.all())
    reference = forms.CharField(label='Reference *')
    invoice_number = forms.CharField(label='Invoice number *')
    po_number = forms.CharField(label='PO number *')
    dr_number = forms.CharField(label='DR number *')


class IRR_entryForm2(forms.Form):
    dce_user = forms.ModelChoiceField(queryset=Employee.objects.all(), label='User *')
    dce_approved = forms.ModelChoiceField(queryset=Employee.objects.all(), label='Approved by *')
    proc_date = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}), label='Proc date *')
    approved_date = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}), label='Approved date*')
    date_dlvrd = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}), label='Delivery date *')

class IRR_entry_cont_Form(forms.ModelForm):

    date_recv = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}), label='Date received *')
    cost_center_no = forms.ModelChoiceField(queryset=Cost_center.objects.all(), label='Cost center *')
    wo_no = forms.CharField(label='WO number *')

    class Meta:
        model = IRR
        fields = ('cost_center_no', 'date_recv' , 'wo_no' , 'remarks',)

class Product_to_IRRForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity_accepted = forms.IntegerField(label='Quantity accepted *')
    quantity_rejected = forms.IntegerField(label='Quantity rejected *')
    quantity_balance = forms.IntegerField(label='Quantity balance *')

class MIV_entryForm(forms.ModelForm):

    date_issued = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}), label='Date issued *')

    class Meta:
        model = MIV
        fields = ( 'date_issued', 'remarks')

#class PAR_entryForm(forms.ModelForm):

    """def __init__(self, irn, *args, **kwargs):
        super(PAR_entryForm, self).__init__(*args, **kwargs)
        self.fields['dce'] = forms.ModelChoiceField(Employee.objects.filter(\
            cost_center_no=IRR.objects.get(irr_no=irn).irr_headkey.inv_station_no.cost_center_no.id))
        self.fields['approved_by'] = forms.ModelChoiceField(Employee.objects.filter(\
            cost_center_no=IRR.objects.get(irr_no=irn).irr_headkey.inv_station_no.cost_center_no.id))
        self.fields['issued_by'] = forms.ModelChoiceField(Employee.objects.filter(\
            cost_center_no=IRR.objects.get(irr_no=irn).irr_headkey.inv_station_no.cost_center_no.id))"""


#    class Meta:
#        model = PAR
#        fields = ('dce', 'par_no', 'approved_by', \
#        'issued_by', 'PO_number', 'date_acquired', 'remark', )

class PAR_Form(forms.ModelForm):

    """def __init__(self, irn, *args, **kwargs):
        super(PAR_Form, self).__init__(*args, **kwargs)
        self.fields['dce'] = forms.ModelChoiceField(Employee.objects.filter(\
            cost_center_no=IRR.objects.get(irr_no=irn).irr_headkey.inv_station_no.cost_center_no.id))
        self.fields['approved_by'] = forms.ModelChoiceField(Employee.objects.filter(\
            cost_center_no=IRR.objects.get(irr_no=irn).irr_headkey.inv_station_no.cost_center_no.id))
        self.fields['issued_by'] = forms.ModelChoiceField(Employee.objects.filter(\
            cost_center_no=IRR.objects.get(irr_no=irn).irr_headkey.inv_station_no.cost_center_no.id))"""

    date_acquired = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}), label='Date acquired*')

    class Meta:
        model = PAR
        fields = ('dce', 'approved_by', 'date_acquired', 'remarks',)


class Product_to_PARForm(forms.Form):

    """def __init__(self, irn, *args, **kwargs):
        super(Product_to_PARForm, self).__init__(*args, **kwargs)
        products = IRR.objects.get(irr_no=irn).product
        self.fields['product'] = forms.ModelChoiceField(Product.objects.all().filter(id__in=\"
            [Product.objects.get(id=p['Product']).id for p in products]))"""

    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, label='Product *')
    quantity = forms.IntegerField(required=True, label='Quantity *')
    par_no = forms.CharField(required=True, label='PAR number *')


class Product_to_PARForm1(forms.Form):

    """def __init__(self, irn, *args, **kwargs):
        super(Product_to_PARForm, self).__init__(*args, **kwargs)
        products = IRR.objects.get(irr_no=irn).product
        self.fields['product'] = forms.ModelChoiceField(Product.objects.all().filter(id__in=\"
            [Product.objects.get(id=p['Product']).id for p in products]))"""

    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, label='Product *')
    quantity = forms.IntegerField(required=True, label='Quantity *')

class GARV_entryForm(forms.ModelForm):

    date_inspected = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}), label='Date inspected *')
    date_confirmed = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}), label='Date confirmed *')
    cc_number = forms.CharField(label='CC number *')
    inspected_by = forms.CharField(label='Inspected by *')
    confirmed_by = forms.CharField(label='Confirmed by *')
    noted_by = forms.CharField(label='Noted by *')

    class Meta:
        model = GARV
        fields = ('cc_number', \
                    'inspected_by', 'date_inspected', 'confirmed_by', \
                    'date_confirmed', 'noted_by', )

#class GARV_Form(forms.ModelForm):

#    class Meta:
#        model = GARV
#        fields = ('cc_number', 'inspected_by', 'date_inspected', \
#        'confirmed_by', 'date_confirmed', 'noted_by', )

    """def __init__(self, pk, *args, **kwargs):
       super(GARV_Form, self).__init__(*args, **kwargs)
       self.fields['product'].queryset = PAR.objects.all().filter(par_no=pk)"""


class Product_to_GARVform(forms.Form):

    product = forms.ModelChoiceField(queryset=PAR.objects.all(), label='Product *')
    quantity = forms.IntegerField(label='Quantity *')
    remarks = forms.CharField(required=False)
    garv_no = forms.CharField(required=True, label='GARV number *')

    """def __init__(self, var, *args, **kwargs):
       super(Product_to_GARVform, self).__init__(*args, **kwargs)
       self.fields['product'].queryset = var"""

class Product_to_GARVform1(forms.Form):

    product = forms.ModelChoiceField(queryset=PAR.objects.all(), label='Product *')
    quantity = forms.IntegerField(label='Quantity *')
    remarks = forms.CharField(required=False)

    """def __init__(self, var, *args, **kwargs):
       super(Product_to_GARVform, self).__init__(*args, **kwargs)
       self.fields['product'].queryset = var"""
