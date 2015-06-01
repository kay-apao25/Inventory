"""forms"""
from django import forms
from WISH.models import Supplier, Product, PAR, GARV, CostCenter, \
        InventoryStat, Employee, IRRHeader, IRR, MIV, WRSPending
from bootstrap3_datetime.widgets import DateTimePicker
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory

class ProductForm(forms.ModelForm):
    """ProductForm"""

    class Meta:
        """Meta"""
        model = Product
        exclude = ('item_name', 'nsn', \
            'generic_name', 'brand', 'part_number', 'manufacture_date',\
             'expiry_date', 'classification', \
            'stock', 'block', 'unit_measure', 'unit_cost', 'quantity', \
            'average_amount', 'status', 'balance_limit', 'serial_number',\
            'model', 'description', 'remarks', \
            'purchased_from', 'inv_station_no',\
            'slc_number', 'amount', 'balance', 'is_irr')


class ProductForm1(forms.Form):
    """ProductForm1"""
    nsn = forms.CharField(label='NSN *', max_length=10, required=True)
    generic_name = forms.CharField(label='Generic name *', max_length=25, required=True)
    item_name = forms.CharField(label='Item name*', max_length=10, required=True)
    brand = forms.CharField(label='Brand *', max_length=25, required=True)
    part_number = forms.CharField(label='Part number *', max_length=8, required=True)
    manufacture_date = forms.DateField(label='Manufacture date *',\
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",\
         "pickTime": False}), required=True)
    expiry_date = forms.DateField(widget=DateTimePicker(\
        options={"format": "YYYY-MM-DD", "pickTime": False}), required=False)
    """inv_station_no = forms.ModelChoiceField(label=\
        'Inventory station *', queryset=\
        InventoryStat.objects.filter(is_delete=False), required=True)"""

class ProductForm2(forms.Form):
    """ProductForm2"""
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

    

    unit_cost = forms.DecimalField(label='Unit cost*', decimal_places=2, required=True)
    quantity = forms.IntegerField(min_value=0, initial='1', label='Quantity *', required=True)
    classification = forms.CharField(label='Classification*', max_length=30, required=True)
    stock = forms.CharField(label='Stock *', max_length=10, required=True)
    block = forms.CharField(label='Block *', max_length=10, required=True)
    unit_measure = forms.ChoiceField(label='Unit measure *',\
     choices=UNIT_CHOICES, required=True)
    status = forms.ChoiceField(label='Status *', choices=STATUS_CHOICES, required=True)

class ProductForm3(forms.Form):
    """ProductForm3"""
    """purchased_from = forms.ModelChoiceField(\
        queryset=Supplier.objects.filter(is_delete=False), \
        label='Purchased from *', required=True)"""
    average_amount = forms.FloatField(label='Average amount *', required=True)
    balance_limit = forms.FloatField(label='Balance limit *', required=True)
    serial_number = forms.CharField(max_length=15, required=False)
    model = forms.CharField(label='Model *', max_length=25, required=True)
    description = forms.CharField(label='Description*', max_length=25, required=True)
    remarks = forms.CharField(max_length=25, required=False)

class ProductForm5(forms.ModelForm):
    """ProductForm5"""

    class Meta:
        """Meta"""
        model = Product
        fields = ('item_name', 'nsn', 'generic_name',\
         'brand', 'part_number', 'manufacture_date', \
         'expiry_date', 'classification', \
        'stock', 'block', 'unit_measure', 'unit_cost', 'quantity', \
        'average_amount', 'status', 'balance_limit', 'serial_number',\
        'model', 'description', 'remarks', 'purchased_from', 'inv_station_no', \
        'slc_number', 'amount',)

class IRRentryForm(forms.ModelForm):
    """IRRHeader"""
    class Meta:
        """Meta"""
        model = IRRHeader
        exclude = ('inv_station_no', 'supplier', 'reference', \
            'invoice_number', 'po_number', 'dr_number',\
            'pr_number', 'dce_custodian', 'dce_user', 'dce_approved',\
             'proc_date', 'approved_date', 'type_n', 'date_dlvrd',)


class IRRentryForm1(forms.Form):
    """IRR_entryForm1"""

    supplier = forms.ModelChoiceField(label='Supplier *',\
     queryset=Supplier.objects.filter(is_delete=False), required=True)
    reference = forms.CharField(label='Reference *', required=True)
    invoice_number = forms.CharField(label='Invoice number *', required=True)
    po_number = forms.CharField(label='PO number *', required=True)
    pr_number = forms.CharField(label='PR number *', required=True)

    class Meta:
        unique_together = (('supplier', 'po_number', 'pr_number'), )

class IRRentryForm2(forms.Form):
    """IRR_entryForm2"""

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name')
        super(IRRentryForm2, self).__init__(*args, **kwargs)

        self.fields['dce_user'] = forms.ModelChoiceField(\
            queryset=Employee.objects.filter(\
            is_delete=False).filter(cost_center_no=Employee.objects.get(\
                name=name).cost_center_no), label='End User *', required=True)
        self.fields['dce_approved'] = forms.ModelChoiceField(\
            queryset=Employee.objects.filter(\
            is_delete=False).filter(cost_center_no=Employee.objects.get(\
                name=name).cost_center_no), label='Approved by *', required=True)
        self.fields['proc_date'] = forms.DateField(widget=DateTimePicker(\
        options={"format": "YYYY-MM-DD", "pickTime": False}), \
        label='Proc date *', required=True)
        self.fields['approved_date'] = forms.DateField(widget=DateTimePicker(\
        options={"format": "YYYY-MM-DD", "pickTime": False}),\
         label='Approved date*', required=True)
        self.fields['date_dlvrd'] = forms.DateField(widget=DateTimePicker(\
        options={"format": "YYYY-MM-DD", "pickTime": False}), \
        label='Delivery date *', required=True)

    dr_number = forms.CharField(label='DR number *', required=True)

class IRRentrycontForm(forms.ModelForm):
    """IRR_entry_cont_Form"""

    date_recv = forms.DateField(widget=DateTimePicker(options=\
        {"format": "YYYY-MM-DD", "pickTime": False}), label='Date received *', required=True)
    wo_no = forms.CharField(label='WO number *', required=True)

    class Meta:
        model = IRR
        fields = ('date_recv', 'wo_no', 'remarks',)

class ProductCheckForm(forms.Form):
    def __init__(self, *args, **kwargs):
        inv = kwargs.pop('inv')
        sup = kwargs.pop('sup')
        q = kwargs.pop('q')
        plist = kwargs.pop('plist')
        super(ProductCheckForm, self).__init__(*args, **kwargs)

        self.fields['product'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,\
            required=True, label='', queryset=Product.objects.filter(inv_station_no=inv).filter(\
            purchased_from=sup).filter(quantity__gt=0).filter(slc_number__contains=q).exclude(id__in=[p.id for p in plist]))
        self.fields['product'].widget.attrs = {'id': 'myCustomId'}

class SupplierCheckForm(forms.Form):
    def __init__(self, *args, **kwargs):
        inv = kwargs.pop('inv')
        q = kwargs.pop('q')
        super(SupplierCheckForm, self).__init__(*args, **kwargs)

        self.fields['purchased_from'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,\
            required=True, label='', queryset=Supplier.objects.filter(supplier_name__contains=q))
        self.fields['purchased_from'].widget.attrs = {'id': 'myCustomId'}

class ProductCheckForm1(forms.Form):
    def __init__(self, *args, **kwargs):
        inv = kwargs.pop('inv')
        q = kwargs.pop('q')
        plist = kwargs.pop('plist')
        super(ProductCheckForm1, self).__init__(*args, **kwargs)

        self.fields['product'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,\
            required=True, queryset=Product.objects.filter(inv_station_no=inv).\
            filter(slc_number__contains=q).filter(is_irr=True).exclude(id__in=[p.id for p in plist]))

class MIVentryForm(forms.ModelForm):
    """MIV_entryForm"""

    date_issued = forms.DateField(widget=DateTimePicker(\
        options={"format": "YYYY-MM-DD", "pickTime": False}), \
        label='Date issued *', required=True)

    class Meta:
        """Meta"""
        model = MIV
        fields = ('date_issued', 'remarks',)

class PARForm(forms.ModelForm):
    """PAR_Form"""

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name')
        super(PARForm, self).__init__(*args, **kwargs)

        self.fields['dce'] = forms.ModelChoiceField(\
            queryset=Employee.objects.filter(\
            cost_center_no=Employee.objects.get(name=name).cost_center_no.id),
            label='Accountable Employee*', required=True)
        self.fields['approved_by'] = forms.ModelChoiceField(\
            queryset=Employee.objects.filter(\
        cost_center_no=Employee.objects.get(name=name).cost_center_no.id),
        label='Approved by*', required=True)

    date_acquired = forms.DateField(widget=DateTimePicker(\
        options={"format": "YYYY-MM-DD", "pickTime": False}),\
         label='Date acquired*', required=True)

    class Meta:
        """Meta"""
        model = PAR
        fields = ('par_no', 'dce', 'approved_by', 'date_acquired', 'remarks',)


class ProducttoPARForm(forms.Form):
    """Product_to_PARForm"""
    def __init__(self, *args, **kwargs):
        prodlist = kwargs.pop('prodlist')
        super(ProducttoPARForm, self).__init__(*args, **kwargs)

        self.fields['product'] = forms.ModelChoiceField(\
            queryset=Product.objects.all().filter(id__in=\
        [Product.objects.get(id=p).id for p in prodlist])\
        , label='Product *', required=True)
        self.fields['quantity'] = forms.IntegerField(\
            min_value=0, required=True, label='Quantity *')

class GARVentryForm(forms.ModelForm):
    """GARV_entryForm"""

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        super(GARVentryForm, self).__init__(*args, **kwargs)

        self.fields['cc_number'] = forms.ModelChoiceField(\
            queryset=CostCenter.objects.all(), label='CC number *', required=True)

        self.fields['inspected_by'] = forms.ModelChoiceField(\
            queryset=Employee.objects.all(), label='Inspected by *', required=True)

        self.fields['noted_by'] = forms.ModelChoiceField(\
            queryset=Employee.objects.all(), label='Noted by *', required=True)

    date_inspected = forms.DateField(widget=DateTimePicker\
        (options={"format": "YYYY-MM-DD", "pickTime": False}), \
        label='Date inspected*', required=True)
    date_confirmed = forms.DateField(widget=DateTimePicker\
        (options={"format": "YYYY-MM-DD", "pickTime": False}), \
        label='Date confirmed *', required=True)

    class Meta:
        """Meta"""
        model = GARV
        fields = ('garv_no', 'cc_number', 'inspected_by', 'noted_by',\
            'date_confirmed', 'date_inspected', )

class ProducttoGARVform(forms.Form):

    """Product_to_GARVform"""

    def __init__(self, *args, **kwargs):
        prodlist = kwargs.pop('prodlist')
        super(ProducttoGARVform, self).__init__(*args, **kwargs)

        self.fields['product'] = forms.ModelChoiceField(\
            queryset=Product.objects.all().filter(id__in=\
        [Product.objects.get(id=p).id for p in prodlist]),\
            label='Product *', required=True)
        self.fields['quantity'] = forms.IntegerField(\
            min_value=0, required=True, label='Quantity *')
        self.fields['remarks'] = forms.CharField(required=False)

class Statlib(forms.ModelForm):
    """Stat_lib"""

    inv_station_no = forms.CharField(label='Inventory station no*', required=True)
    station_description = forms.CharField(label='Station description*', required=True)

    class Meta:
        model = InventoryStat
        fields = ('inv_station_no', 'station_description', 'cost_center_no',)

class Statlib1(forms.ModelForm):
    """Stat_lib"""

    station_description = forms.CharField(label='Station description*', required=True)

    class Meta:
        model = InventoryStat
        fields = ( 'station_description', 'cost_center_no',)


class CClib(forms.ModelForm):
    """CC_lib"""

    cost_center_name = forms.CharField(label='Cost center name*', required=True)
    functional_group = forms.CharField(label='Functional group*', required=True)

    class Meta:
        """Meta"""
        model = CostCenter
        fields = ('cost_center_name', 'functional_group',)

class Supplierlib(forms.ModelForm):

    """Supplier_lib"""
    class Meta:
        """Meta"""
        model = Supplier
        fields = ('supplier_name', 'supplier_address', 'telephone_number',\
        'credit_limit', 'debit_amount', 'credit_amount', 'balance_amount', \
        'contact_person', 'remarks',)

class Supplierlib1(forms.ModelForm):
    """Supplier_lib1"""
    class Meta:
        """Meta"""
        model = Supplier
        fields = ('telephone_number', 'credit_limit', \
            'supplier_name', 'supplier_address', )
class Supplierlib2(forms.ModelForm):
    """Supplier_lib2p"""
    class Meta:
        model = Supplier
        fields = ('debit_amount', 'credit_amount', \
            'balance_amount', 'contact_person', 'remarks',)

class Suplib(forms.ModelForm):
    """Sup_lib"""
    class Meta:
        model = Supplier
        fields = ('supplier_number', 'supplier_name', 'supplier_address'\
        , 'telephone_number', 'credit_limit', 'debit_amount', 'credit_amount',\
         'balance_amount', 'contact_person', 'remarks',)

class Suplib1(forms.ModelForm):
    """Sup_lib1"""
    class Meta:
        model = Supplier
        fields = ('supplier_number', 'telephone_number', 'credit_limit',\
         'supplier_name', 'supplier_address', )

class Suplib2(forms.ModelForm):
    """Sup_lib2"""
    class Meta:
        model = Supplier
        fields = ('debit_amount', 'credit_amount', 'balance_amount', \
            'contact_person', 'remarks',)

class Employeelib(forms.ModelForm):
    """Employee_lib"""
    cost_center_no = forms.ModelChoiceField(\
        queryset=CostCenter.objects.filter(is_delete=False), required=True)
    class Meta:
        model = Employee
        fields = ('name', 'position', 'cost_center_no', 'charging_cc_no',)

class Emlib(forms.ModelForm):
    """Em_lib"""
    cost_center_no = forms.ModelChoiceField(\
        queryset=CostCenter.objects.filter(is_delete=False), required=True)
    class Meta:
        model = Employee
        fields = ('dce', 'name', 'position', 'cost_center_no',\
         'charging_cc_no',)

class LoginForm(forms.Form):
    """LoginForm"""
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class SignUpForm(forms.Form):
    """SignUpForm"""
    dce = forms.CharField(max_length=255, required=True)
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    username1 = forms.CharField(label='Username', max_length=255, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')

class GuestForm(forms.Form):
    """GuestForm"""
    dce = forms.CharField(max_length=255, required=True)

class WRSPendingForm(forms.ModelForm):
    """WRSPendingForm"""
    class Meta:
        model = WRSPending
        exclude = ('product', 'inv_station_no', 'cost_center_no', 'wrs_number',)

class ProductWRS(forms.Form):
    """ProductWRS"""
    def __init__(self, *args, **kwargs):
        inv = kwargs.pop('inv')
        super(ProductWRS, self).__init__(*args, **kwargs)

        self.fields['product'] = forms.ModelChoiceField(\
            queryset=Product.objects.filter(\
            inv_station_no=inv).filter(quantity__gt=0), label='Product *',\
             required=True)
        self.fields['qty'] = forms.IntegerField(min_value=0,\
         label='Quantity*', required=True)
