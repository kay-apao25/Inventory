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
            'model', 'description', 'remark', 'purchased_from', 'inv_station_no', \
            'slc_number', 'amount', )

class ProductForm1(forms.Form):
    nsn = forms.CharField(max_length=10)
    product_number = forms.CharField(max_length=10)
    generic_name = forms.CharField(max_length=25)
    item_name = forms.CharField(max_length=10)
    brand = forms.CharField(max_length=25)
    part_number = forms.CharField(max_length=8)
    manufacture_date = forms.DateField()
    inv_station_no = forms.ModelChoiceField(queryset=Inventory_stat.objects.all())

class ProductForm2(forms.Form):
    UNIT_CHOICES = (
        ('unit', 'unit'),
        ('piece', 'piece'),
        ('box', 'box'),
        ('pack', 'pack'),
        ('pad', 'pad'),
        ('ream', 'ream'),
    )
    expiry_date = forms.DateField(required=False)
    unit_cost = forms.DecimalField(decimal_places=2)
    quantity = forms.IntegerField(initial='1')
    classification = forms.CharField(max_length=30)
    stock = forms.CharField(max_length=10)
    block = forms.CharField(max_length=10)
    unit_measure = forms.ChoiceField(choices=UNIT_CHOICES)
    status = forms.CharField(max_length=10, initial='Pending')

class ProductForm3(forms.Form):
    purchased_from = forms.ModelChoiceField(queryset=Supplier.objects.all())
    average_amount = forms.FloatField()
    balance_limit = forms.FloatField()
    serial_number = forms.CharField(max_length=15)
    model = forms.CharField(max_length=25)
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
    quantity_accepted = forms.IntegerField()
    quantity_rejected = forms.IntegerField()
    quantity_balance = forms.IntegerField()

class MIV_entryForm(forms.ModelForm):

    class Meta:
        model = MIV
        fields = ( 'date_issued', 'remark')

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

    class Meta:
        model = PAR
        fields = ('dce', 'approved_by', 'issued_by', 'date_acquired', 'remark',)


class Product_to_PARForm(forms.Form):

    """def __init__(self, irn, *args, **kwargs):
        super(Product_to_PARForm, self).__init__(*args, **kwargs)
        products = IRR.objects.get(irr_no=irn).product
        self.fields['product'] = forms.ModelChoiceField(Product.objects.all().filter(id__in=\"
            [Product.objects.get(id=p['Product']).id for p in products]))"""

    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=True)
    quantity = forms.IntegerField(required=True)
    par_no = forms.CharField(required=True)


class Product_to_PARForm1(forms.Form):

    """def __init__(self, irn, *args, **kwargs):
        super(Product_to_PARForm, self).__init__(*args, **kwargs)
        products = IRR.objects.get(irr_no=irn).product
        self.fields['product'] = forms.ModelChoiceField(Product.objects.all().filter(id__in=\"
            [Product.objects.get(id=p['Product']).id for p in products]))"""

    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=True)
    quantity = forms.IntegerField(required=True)

class GARV_entryForm(forms.ModelForm):

    class Meta:
        model = GARV
        fields = ('cc_number', \
                    'inspected_by', 'date_inspected', 'confirmed_by', \
                    'date_confirmed', 'noted_by', )

class GARV_Form(forms.ModelForm):

    class Meta:
        model = GARV
        fields = ('cc_number', 'inspected_by', 'date_inspected', \
        'confirmed_by', 'date_confirmed', 'noted_by', )

    """def __init__(self, pk, *args, **kwargs):
       super(GARV_Form, self).__init__(*args, **kwargs)
       self.fields['product'].queryset = PAR.objects.all().filter(par_no=pk)"""


class Product_to_GARVform(forms.Form):

    product = forms.ModelChoiceField(queryset=PAR.objects.all())
    quantity = forms.IntegerField()
    remarks = forms.CharField()
    garv_no = forms.CharField(required=True)

    """def __init__(self, var, *args, **kwargs):
       super(Product_to_GARVform, self).__init__(*args, **kwargs)
       self.fields['product'].queryset = var"""

class Product_to_GARVform1(forms.Form):

    product = forms.ModelChoiceField(queryset=PAR.objects.all())
    quantity = forms.IntegerField()
    remarks = forms.CharField()

    """def __init__(self, var, *args, **kwargs):
       super(Product_to_GARVform, self).__init__(*args, **kwargs)
       self.fields['product'].queryset = var"""
