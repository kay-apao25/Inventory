from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Supplier(models.Model):
    supplier_number = models.CharField(max_length=8)
    supplier_name = models.TextField(max_length=20)
    supplier_address = models.TextField(max_length=20)
    telephone_number = models.CharField(max_length=20)
    credit_limit = models.FloatField()
    debit_amount = models.FloatField()
    credit_amount = models.FloatField()
    balance_amount = models.FloatField()
    contact_person = models.TextField(max_length=20)
    remarks = models.TextField(max_length=20)

    def __str__(self):
        return self.supplier_name + ", " + self.supplier_address + ", " + self.supplier_number

class Cost_center(models.Model):
    cost_center_name = models.TextField(max_length=20)
    functional_group = models.CharField(max_length=20)

    def __str__(self):
        return self.cost_center_name

class Inventory_stat(models.Model):
    inv_station_no = models.CharField(max_length = 20, primary_key = True)
    station_description = models.TextField()
    cost_center_no = models.ForeignKey(Cost_center)

    def __str__(self):
        return self.station_description


class Employee(models.Model):
    dce = models.CharField(max_length=8, primary_key = True)
    name = models.TextField()
    cost_center_no = models.ForeignKey(Cost_center)
    charging_cc_no = models.CharField(max_length=20)
    position = models.TextField()

    def __str__(self):
        return self.name

class Customer(models.Model):
    dce = models.ForeignKey(Employee)
    credit_limit = models.FloatField()
    debit_amount = models.FloatField()
    credit_amount = models.FloatField()
    balance_amount = models.FloatField()

    def __str__(self):
        return self.dce

class IRR_header(models.Model):
    inv_station_no = models.ForeignKey(Inventory_stat)
    reference = models.CharField(max_length=20)
    invoice_number = models.CharField(max_length=20)
    po_number = models.CharField(max_length=20)
    dr_number = models.CharField(max_length=20)
    dce_custodian = models.ForeignKey(Employee, related_name='dce1')
    dce_user = models.ForeignKey(Employee, related_name='dce2')
    proc_date = models.DateField()
    type_n = models.CharField(max_length=20)
    date_dlvrd = models.DateField()
    supplier = models.ForeignKey(Supplier)

    def __str__(self):
        return str(self.id)

class IRR(models.Model):
    irr_headkey = models.ForeignKey(IRR_header)
    irr_no = models.IntegerField(primary_key = True)
    cost_center_no = models.ForeignKey(Cost_center)
    quantity_actual = models.FloatField()
    quantity_accepted = models.FloatField()
    quantity_rejected = models.FloatField()
    quantity_balance = models.FloatField()
    date_recv = models.DateField(blank = True, null = True)
    wo_no = models.CharField(max_length=7)
    remark = models.TextField(max_length = 30)

    def __unicode__(self):
        return str(self.irr_no)

class Product(models.Model):
    nsn = models.CharField(max_length=10)
    product_number = models.CharField(max_length=10)
    slc_number = models.IntegerField()
    inv_station_no = models.ForeignKey(Inventory_stat)
    cost_center_no = models.ForeignKey(Cost_center)
    item_name = models.TextField()
    generic_name = models.TextField()
    brand = models.TextField()
    part_number = models.CharField(max_length=8)
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    classification = models.CharField(max_length=30)
    stock = models.CharField(max_length=10)
    block = models.CharField(max_length=10)
    unit_measure = models.CharField(max_length=10)
    unit_cost = models.FloatField()
    quantity = models.FloatField(default = '1')
    average_amount = models.FloatField()
    status = models.CharField(max_length=10)
    balance_limit = models.FloatField()
    serial_number = models.CharField(max_length=15)
    model = models.TextField()
    amount = models.FloatField()
    description = models.TextField()
    remark = models.TextField()
    purchased_from = models.ForeignKey(Supplier)
    irr_no = models.ForeignKey(IRR)

    def __str__(self):
        return self.item_name + " , " + self.description

class MIV(models.Model):
    irr_no = models.ForeignKey(IRR_header)
    inv_station_no = models.ForeignKey(Inventory_stat)
    asset_code = models.ForeignKey(Product)
    cost_center_no = models.ForeignKey(Cost_center)
    wrs_number = models.CharField(max_length = 8)
    cost_center_no = models.ForeignKey(Cost_center)
    quantity = models.FloatField()
    amount = models.FloatField()
    date_issued = models.DateField(blank = True, null = True)
    doc_date = models.DateField(blank = True, null = True)
    remark = models.TextField()

    def __str__(self):
        return str(self.irr_no) + ", " + str(self.asset_code)

class PAR(models.Model):
    dce = models.ForeignKey(Employee)
    asset_code = models.ForeignKey(Product)
    par_date = models.DateField(blank=True, null=True)
    par_no = models.CharField(max_length=10, null=True)
    amt_cost = models.FloatField()
    remark = models.TextField()
    qty = models.IntegerField()
    approved_by = models.ForeignKey(Employee, related_name='dce_FK2')
    issued_by = models.ForeignKey(Employee, related_name='dce_FK3')
    inv_stat_no = models.ForeignKey(Inventory_stat)
    PO_number = models.ForeignKey(IRR_header)
    date_acquired = models.DateField(blank=True, null=True)
    wo_number = models.ForeignKey(IRR)


    class Meta:
        unique_together = (("dce", "asset_code"))

    def __str__(self):
        return self.par_no

class GARV(models.Model):
    dce = models.ForeignKey(Employee)
    asset_code = models.ForeignKey(Product)
    garv_date = models.DateField(blank=True, null=True)
    garv_no = models.CharField(max_length=10, null=True)
    cc_number = models.ForeignKey(Cost_center)
    wo_number = models.ForeignKey(IRR_header)
    qty = models.CharField(max_length=20, null=True)
    par_number = models.ForeignKey(PAR)
    remarks = models.CharField(max_length=20, null=True)
    inspected_by = models.ForeignKey(Employee, related_name='dce_FK4')
    date_inspected = models.DateField(blank=True, null=True)
    confirmed_by = models.ForeignKey(Employee, related_name='dce_FK5')
    date_confirmed = models.DateField(blank=True, null=True)
    noted_by = models.ForeignKey(Employee, related_name='dce_FK6')

    class Meta:
        unique_together = ('dce', 'asset_code')

    def __str__(self):
        return str(self.dce) + "," + str(self.asset_code)

class Pending(models.Model):
    item_name = models.TextField()
    supplier_number = models.ForeignKey(Supplier)
    serial_number = models.CharField(max_length=10)
    model = models.TextField()
    amount = models.FloatField()
    description = models.TextField()

    class Meta:
        unique_together = ('supplier_number', 'serial_number', 'model')

    def __str__(self):
        return self.supplier_number + "," + self.serial_number + "," + self.model



