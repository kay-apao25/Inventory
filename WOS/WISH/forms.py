from django import forms
from .forms import *
from .views import *
from django.db.models import Q
from bootstrap3_datetime.widgets import DateTimePicker
from django.contrib import auth

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('product_number', 'item_name', 'nsn', 'generic_name', 'brand',\
            'part_number', 'manufacture_date', 'expiry_date', 'classification', \
            'stock', 'block', 'unit_measure', 'unit_cost', 'quantity', \
            'average_amount', 'status', 'balance_limit', 'serial_number',\
            'model', 'description', 'remarks', 'purchased_from', 'inv_station_no', \
            'slc_number', 'amount', 'balance', 'is_irr')



class ProductForm1(forms.Form):
    nsn = forms.CharField(label='NSN *', max_length=10)
    product_number = forms.CharField(label='Product number *', max_length=10)
    generic_name = forms.CharField(label='Generic name *', max_length=25)
    item_name = forms.CharField(label='Item name*', max_length=10)
    brand = forms.CharField(label='Brand *', max_length=25)
    part_number = forms.CharField(label='Part number *', max_length=8)
    manufacture_date = forms.DateField(label='Manufacture date *',
        widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}))
    inv_station_no = forms.ModelChoiceField(label='Inventory station *', queryset=Inventory_stat.objects.filter(is_delete=False))

class ProductForm2(forms.Form):
    UNIT_CHOICES = (
        ('unit', 'unit'),
        ('piece', 'piece'),
        ('box', 'box'),
        ('pack', 'pack'),
        ('pad', 'pad'),
        ('ream', 'ream'),
    )
    STATUS_CHOICES = (
        ('Complete', 'Complete'),
        ('Pending', 'Pending'),
    )

    expiry_date = forms.DateField(widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}), required=False)
    unit_cost = forms.DecimalField(label='Unit cost*', decimal_places=2)
    quantity = forms.IntegerField(min_value=0, initial='1', label='Quantity *')
    classification = forms.CharField(label='Classification*', max_length=30)
    stock = forms.CharField(label='Stock *', max_length=10)
    block = forms.CharField(label='Block *', max_length=10)
    unit_measure = forms.ChoiceField(label='Unit measure *', choices=UNIT_CHOICES)
    status = forms.ChoiceField(label='Status *', choices=STATUS_CHOICES)

class ProductForm3(forms.Form):
    purchased_from = forms.ModelChoiceField(queryset=Supplier.objects.filter(is_delete=False), label='Purchased from *')
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
            'slc_number', 'amount',)

class IRR_entryForm(forms.ModelForm):
    class Meta:
        model = IRR_header
        exclude = ('inv_station_no', 'supplier', 'reference', 'invoice_number', 'po_number', 'dr_number',\
                    'pr_number', 'dce_custodian', 'dce_user', 'dce_approved','proc_date', 'approved_date','type_n', 'date_dlvrd',)


class IRR_entryForm1(forms.Form):

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name')
        super(IRR_entryForm1, self).__init__(*args, **kwargs)
        self.fields['inv_station_no'] = forms.ModelChoiceField(queryset=Inventory_stat.objects.filter(\
                cost_center_no=Employee.objects.get(name=name).cost_center_no).filter(\
                id__in=[p.inv_station_no.id for p in Product.objects.filter(is_irr=False)]), label='Inventory Station *')

    supplier = forms.ModelChoiceField(label='Supplier *', queryset=Supplier.objects.filter(is_delete=False))
    reference = forms.CharField(label='Reference *')
    invoice_number = forms.CharField(label='Invoice number *')
    po_number = forms.CharField(label='PO number *')
    dr_number = forms.CharField(label='DR number *')


class IRR_entryForm2(forms.Form):

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name')
        super(IRR_entryForm2, self).__init__(*args, **kwargs)

        self.fields['dce_user'] = forms.ModelChoiceField(queryset=Employee.objects.filter(\
            is_delete=False).filter(cost_center_no=Employee.objects.get(\
                name=name).cost_center_no), label='User *')
        self.fields['dce_approved'] = forms.ModelChoiceField(queryset=Employee.objects.filter(\
            is_delete=False).filter(cost_center_no=Employee.objects.get(\
                name=name).cost_center_no), label='Approved by *')
        self.fields['proc_date'] = forms.DateField(widget=DateTimePicker(\
            options={"format": "YYYY-MM-DD", "pickTime": False}), label='Proc date *')
        self.fields['approved_date'] = forms.DateField(widget=DateTimePicker(options={\
            "format": "YYYY-MM-DD", "pickTime": False}), label='Approved date*')
        self.fields['date_dlvrd'] = forms.DateField(widget=DateTimePicker(options={\
            "format": "YYYY-MM-DD", "pickTime": False}), label='Delivery date *')

    pr_number = forms.CharField(label='PR number *')

class IRR_entry_cont_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        inv = kwargs.pop('inv')
        super(IRR_entry_cont_Form, self).__init__(*args, **kwargs)

        self.fields['cost_center_no'] = forms.ModelChoiceField(queryset=Cost_center.objects.filter(\
            is_delete=False).filter(cc_iFK__in=[i.cost_center_no.id for i in (Inventory_stat.objects.filter(inv_station_no=inv))]),\
            label='Cost center *')

    date_recv = forms.DateField(widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}), label='Date received *')
    wo_no = forms.CharField(label='WO number *')

    class Meta:
        model = IRR
        fields = ('cost_center_no', 'date_recv' , 'wo_no' , 'remarks',)

class Product_to_IRRForm(forms.Form):

    def __init__(self, *args, **kwargs):
        inv = kwargs.pop('inv')
        super(Product_to_IRRForm, self).__init__(*args, **kwargs)

        self.fields['product'] = forms.ModelChoiceField(queryset=Product.objects.filter(\
            inv_station_no=inv).filter(is_irr=False), label='Product *', required=True)
        self.fields['quantity_accepted'] = forms.IntegerField(min_value=0, label='Quantity accepted *', required=True)
        self.fields['quantity_rejected'] = forms.IntegerField(min_value=0, label='Quantity rejected *', required=True)
        self.fields['quantity_balance'] = forms.IntegerField(min_value=0, label='Quantity balance *', required=True)

class MIV_entryForm(forms.ModelForm):

    date_issued = forms.DateField(widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}), \
        label='Date issued *', required=True)

    class Meta:
        model = MIV
        fields = ( 'date_issued', 'remarks')

class PAR_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        inv = kwargs.pop('inv')
        super(PAR_Form, self).__init__(*args, **kwargs)

        self.fields['dce'] = forms.ModelChoiceField(queryset=Employee.objects.filter(\
            cost_center_no=IRR.objects.get(irr_no=inv).irr_headkey.inv_station_no.cost_center_no.id),\
            label='Accountable Employee*')
        self.fields['approved_by'] = forms.ModelChoiceField(queryset=Employee.objects.filter(\
        cost_center_no=IRR.objects.get(irr_no=inv).irr_headkey.inv_station_no.cost_center_no.id), label='Approved by*')

    date_acquired = forms.DateField(widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}), label='Date acquired*')

    class Meta:
        model = PAR
        fields = ('par_no', 'dce', 'approved_by', 'date_acquired', 'remarks',)


class Product_to_PARForm(forms.Form):

     def __init__(self, *args, **kwargs):
        prodlist = kwargs.pop('prodlist')
        super(Product_to_PARForm, self).__init__(*args, **kwargs)

        self.fields['product'] = forms.ModelChoiceField(queryset=Product.objects.all().filter(id__in=\
        [Product.objects.get(id=p).id for p in prodlist]), label='Product *', required=True)
        self.fields['quantity'] = forms.IntegerField(min_value=0, required=True, label='Quantity *')

class GARV_entryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        super(GARV_entryForm, self).__init__(*args, **kwargs)

        self.fields['cc_number'] = forms.ModelChoiceField(queryset=Cost_center.objects.filter(\
            id=PAR.objects.get(par_no=pk).inv_stat_no.cost_center_no.id), label='CC number *')

        self.fields['inspected_by'] = forms.ModelChoiceField(queryset=Employee.objects.filter(\
                cost_center_no=IRR.objects.get(irr_no=PAR.objects.get(\
            par_no=pk).wo_number).irr_headkey.inv_station_no.cost_center_no.id), label='Inspected by *')

        self.fields['confirmed_by'] = forms.ModelChoiceField(queryset=Employee.objects.filter(\
                cost_center_no=IRR.objects.get(irr_no=PAR.objects.get(\
            par_no=pk).wo_number).irr_headkey.inv_station_no.cost_center_no.id), label='Confirmed by *')

        self.fields['noted_by'] = forms.ModelChoiceField(queryset=Employee.objects.filter(\
                cost_center_no=IRR.objects.get(irr_no=PAR.objects.get(\
            par_no=pk).wo_number).irr_headkey.inv_station_no.cost_center_no.id), label='Noted by *')

    date_inspected = forms.DateField(widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}), \
        label='Date inspected*')
    date_confirmed = forms.DateField(widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}), \
        label='Date confirmed *')

    class Meta:
        model = GARV
        fields = ('garv_no', 'cc_number', 'inspected_by', 'confirmed_by', 'noted_by',\
                    'date_confirmed','date_inspected', )

class Product_to_GARVform(forms.Form):

    def __init__(self, *args, **kwargs):
        prodlist = kwargs.pop('prodlist')
        super(Product_to_GARVform, self).__init__(*args, **kwargs)

        self.fields['product'] = forms.ModelChoiceField(queryset=Product.objects.all().filter(id__in=\
        [Product.objects.get(id=p).id for p in prodlist]), label='Product *', required=True)
        self.fields['quantity'] = forms.IntegerField(min_value=0, required=True, label='Quantity *')
        self.fields['remarks'] = forms.CharField(required=False)

class Stat_lib(forms.ModelForm):

    cost_center_no = forms.ModelChoiceField(queryset=Cost_center.objects.filter(is_delete=False))

    class Meta:
        model = Inventory_stat
        fields = ('inv_station_no', 'station_description', 'cost_center_no',)

class CC_lib(forms.ModelForm):

    class Meta:
        model = Cost_center
        fields = ('cost_center_name', 'functional_group',)

class Supplier_lib(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = ( 'supplier_name', 'supplier_address', 'telephone_number',
        'credit_limit', 'debit_amount', 'credit_amount', 'balance_amount', 'contact_person',
        'remarks',)

class Supplier_lib1(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = ( 'telephone_number', 'credit_limit', 'supplier_name', 'supplier_address', )
class Supplier_lib2(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = ('debit_amount', 'credit_amount', 'balance_amount', 'contact_person', 'remarks',)

class Sup_lib(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = ( 'supplier_number','supplier_name', 'supplier_address', 'telephone_number',
        'credit_limit', 'debit_amount', 'credit_amount', 'balance_amount', 'contact_person',
        'remarks',)

class Sup_lib1(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = ('supplier_number', 'telephone_number', 'credit_limit', 'supplier_name', 'supplier_address', )

class Sup_lib2(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = ('debit_amount', 'credit_amount', 'balance_amount', 'contact_person', 'remarks',)

class Employee_lib(forms.ModelForm):

    cost_center_no = forms.ModelChoiceField(queryset=Cost_center.objects.filter(is_delete=False))
    class Meta:
        model = Employee
        fields = ( 'name', 'position', 'cost_center_no', 'charging_cc_no',)

class Em_lib(forms.ModelForm):

    cost_center_no = forms.ModelChoiceField(queryset=Cost_center.objects.filter(is_delete=False))
    class Meta:
        model = Employee
        fields = ( 'dce', 'name', 'position', 'cost_center_no', 'charging_cc_no',)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
