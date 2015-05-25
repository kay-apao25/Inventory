"""forms"""
from django import forms
from WISH.models import Supplier, Product, PAR, GARV, CostCenter, \
        InventoryStat, Employee, IRRHeader, IRR, MIV
from bootstrap3_datetime.widgets import DateTimePicker
class ProductForm(forms.ModelForm):
    """ProductForm"""

    class Meta:
        """Meta"""
        model = Product
        exclude = ('product_number', 'item_name', 'nsn', \
            'generic_name', 'brand', 'part_number', 'manufacture_date',\
             'expiry_date', 'classification', \
            'stock', 'block', 'unit_measure', 'unit_cost', 'quantity', \
            'average_amount', 'status', 'balance_limit', 'serial_number',\
            'model', 'description', 'remarks', \
            'purchased_from', 'inv_station_no',\
            'slc_number', 'amount', 'balance', 'is_irr')



class ProductForm1(forms.Form):
    """ProductForm1"""
    nsn = forms.CharField(label='NSN *', max_length=10)
    product_number = forms.CharField(label='Product number *', max_length=10)
    generic_name = forms.CharField(label='Generic name *', max_length=25)
    item_name = forms.CharField(label='Item name*', max_length=10)
    brand = forms.CharField(label='Brand *', max_length=25)
    part_number = forms.CharField(label='Part number *', max_length=8)
    manufacture_date = forms.DateField(label='Manufacture date *',\
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",\
         "pickTime": False}))
    inv_station_no = forms.ModelChoiceField(label=\
        'Inventory station *', queryset=\
        InventoryStat.objects.filter(is_delete=False))

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

    expiry_date = forms.DateField(widget=DateTimePicker(\
        options={"format": "YYYY-MM-DD", "pickTime": False}), required=False)
    unit_cost = forms.DecimalField(label='Unit cost*', decimal_places=2)
    quantity = forms.IntegerField(min_value=0, initial='1', label='Quantity *')
    classification = forms.CharField(label='Classification*', max_length=30)
    stock = forms.CharField(label='Stock *', max_length=10)
    block = forms.CharField(label='Block *', max_length=10)
    unit_measure = forms.ChoiceField(label='Unit measure *',\
     choices=UNIT_CHOICES)
    status = forms.ChoiceField(label='Status *', choices=STATUS_CHOICES)

class ProductForm3(forms.Form):
    """ProductForm3"""
    purchased_from = forms.ModelChoiceField(\
        queryset=Supplier.objects.filter(is_delete=False), \
        label='Purchased from *')
    average_amount = forms.FloatField(label='Average amount *')
    balance_limit = forms.FloatField(label='Balance limit *')
    serial_number = forms.CharField(max_length=15, required=False)
    model = forms.CharField(label='Model *', max_length=25)
    description = forms.CharField(label='Description*', max_length=25)
    remarks = forms.CharField(max_length=25, required=False)

class ProductForm5(forms.ModelForm):
    """ProductForm5"""

    class Meta:
        """Meta"""
        model = Product
        fields = ('product_number', 'item_name', 'nsn', 'generic_name',\
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

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name')
        super(IRRentryForm1, self).__init__(*args, **kwargs)
        self.fields['inv_station_no'] = forms.ModelChoiceField(\
            queryset=InventoryStat.objects.filter(\
        cost_center_no=Employee.objects.get(name=name).cost_center_no).filter(\
            id__in=[p.inv_station_no.id for p in Product.objects.filter\
            (is_irr=False)]), label='Inventory Station *')

    supplier = forms.ModelChoiceField(label='Supplier *',\
     queryset=Supplier.objects.filter(is_delete=False))
    reference = forms.CharField(label='Reference *')
    invoice_number = forms.CharField(label='Invoice number *')
    po_number = forms.CharField(label='PO number *')
    dr_number = forms.CharField(label='DR number *')


class IRRentryForm2(forms.Form):
    """IRR_entryForm2"""

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name')
        super(IRRentryForm2, self).__init__(*args, **kwargs)

        self.fields['dce_user'] = forms.ModelChoiceField(\
            queryset=Employee.objects.filter(\
            is_delete=False).filter(cost_center_no=Employee.objects.get(\
                name=name).cost_center_no), label='User *')
        self.fields['dce_approved'] = forms.ModelChoiceField(\
            queryset=Employee.objects.filter(\
            is_delete=False).filter(cost_center_no=Employee.objects.get(\
                name=name).cost_center_no), label='Approved by *')
        self.fields['proc_date'] = forms.DateField(widget=DateTimePicker(\
        options={"format": "YYYY-MM-DD", "pickTime": False}), \
        label='Proc date *')
        self.fields['approved_date'] = forms.DateField(widget=DateTimePicker(\
        options={"format": "YYYY-MM-DD", "pickTime": False}),\
         label='Approved date*')
        self.fields['date_dlvrd'] = forms.DateField(widget=DateTimePicker(\
        options={"format": "YYYY-MM-DD", "pickTime": False}), \
        label='Delivery date *')

    pr_number = forms.CharField(label='PR number *')

class IRRentrycontForm(forms.ModelForm):
    """IRR_entry_cont_Form"""

    def __init__(self, *args, **kwargs):
        inv = kwargs.pop('inv')
        super(IRRentrycontForm, self).__init__(*args, **kwargs)

        self.fields['cost_center_no'] = forms.ModelChoiceField(\
            queryset=CostCenter.objects.filter(\
            is_delete=False).filter(cc_iFK__in=[i.cost_center_no.id \
            for i in (InventoryStat.objects.filter(inv_station_no=inv))]),\
            label='Cost center *')

    date_recv = forms.DateField(widget=DateTimePicker(options=\
        {"format": "YYYY-MM-DD", "pickTime": False}), label='Date received *')
    wo_no = forms.CharField(label='WO number *')

    class Meta:
        model = IRR
        fields = ('cost_center_no', 'date_recv', 'wo_no', 'remarks',)

class ProducttoIRRForm(forms.Form):
    """Product_to_IRRForm"""

    def __init__(self, *args, **kwargs):
        inv = kwargs.pop('inv')
        super(ProducttoIRRForm, self).__init__(*args, **kwargs)

        self.fields['product'] = forms.ModelChoiceField(\
            queryset=Product.objects.filter(\
            inv_station_no=inv).filter(is_irr=False), label='Product *',\
             required=True)
        self.fields['quantity_accepted'] = forms.IntegerField(min_value=0,\
         label='Quantity accepted *', required=True)
        self.fields['quantity_rejected'] = forms.IntegerField(min_value=0,\
         label='Quantity rejected *', required=True)
        self.fields['quantity_balance'] = forms.IntegerField(min_value=0,\
         label='Quantity balance *', required=True)

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
        inv = kwargs.pop('inv')
        super(PARForm, self).__init__(*args, **kwargs)

        self.fields['dce'] = forms.ModelChoiceField(\
            queryset=Employee.objects.filter(\
            cost_center_no=IRR.objects.get(irr_no=inv).\
            irr_headkey.inv_station_no.cost_center_no.id),\
            label='Accountable Employee*')
        self.fields['approved_by'] = forms.ModelChoiceField(\
            queryset=Employee.objects.filter(\
        cost_center_no=IRR.objects.get(irr_no=inv)\
        .irr_headkey.inv_station_no.cost_center_no.id), label='Approved by*')

    date_acquired = forms.DateField(widget=DateTimePicker(\
        options={"format": "YYYY-MM-DD", "pickTime": False}),\
         label='Date acquired*')

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
        self.fields['quantity'] = forms.IntegerField\
        (min_value=0, required=True, label='Quantity *')

class GARVentryForm(forms.ModelForm):
    """GARV_entryForm"""

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        super(GARVentryForm, self).__init__(*args, **kwargs)

        self.fields['cc_number'] = forms.ModelChoiceField(\
            queryset=CostCenter.objects.filter(\
            id=PAR.objects.get(par_no=pk).inv_stat_no.cost_center_no.id)\
        , label='CC number *')

        self.fields['inspected_by'] = forms.ModelChoiceField(\
            queryset=Employee.objects.filter(\
                cost_center_no=IRR.objects.get(irr_no=PAR.objects.get(\
            par_no=pk).wo_number).irr_headkey.inv_station_no.cost_center_no.id\
                ), label='Inspected by *')

        self.fields['noted_by'] = forms.ModelChoiceField(\
            queryset=Employee.objects.filter(\
                cost_center_no=IRR.objects.get(irr_no=PAR.objects.get(\
            par_no=pk).wo_number).irr_headkey.inv_station_no.cost_center_no.id\
                ), label='Noted by *')

    date_inspected = forms.DateField(widget=DateTimePicker\
        (options={"format": "YYYY-MM-DD", "pickTime": False}), \
        label='Date inspected*')
    date_confirmed = forms.DateField(widget=DateTimePicker\
        (options={"format": "YYYY-MM-DD", "pickTime": False}), \
        label='Date confirmed *')

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

    inv_station_no = forms.CharField(label='Inventory station no*')
    cost_center_no = forms.ModelChoiceField(\
        queryset=CostCenter.objects.filter(is_delete=False), label='Cost center no*')
    station_description = forms.CharField(label='Station description*')

    class Meta:
        model = InventoryStat
        fields = ('inv_station_no', 'station_description', 'cost_center_no',)

class CClib(forms.ModelForm):
    """CC_lib"""

    cost_center_name = forms.CharField(label='Cost center name*')
    functional_group = forms.CharField(label='Functional group*')

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
        queryset=CostCenter.objects.filter(is_delete=False))
    class Meta:
        model = Employee
        fields = ('name', 'position', 'cost_center_no', 'charging_cc_no',)

class Emlib(forms.ModelForm):
    """Em_lib"""
    cost_center_no = forms.ModelChoiceField(\
        queryset=CostCenter.objects.filter(is_delete=False))
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

