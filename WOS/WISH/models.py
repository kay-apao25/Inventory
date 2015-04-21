from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Supplier(models.Model):
    supplier_num = models.CharField(max_length=8)
    supplier_name = models.TextField(max_length=50)
    supplier_address = models.TextField(max_length=50)
    telephone_number = models.CharField(max_length=20)
    credit_limit = models.FloatField()
    debit_amt = models.FloatField()
    credit_amt = models.FloatField()
    balance_amt = models.FloatField()
    contact_person = models.TextField(max_length=50)
    remarks = models.TextField(max_length=100)

    def __str__(self):
        return self.supplier_name + ", " + self.supplier_address + ", " + self.supplier_num

class Cost_center(models.Model):
    cost_center_name = models.TextField(max_length=50)
    functional_group = models.CharField(max_length=30)

    def __str__(self):
        return self.cost_center_name

class Inventory_stat(models.Model):
    inv_station_no = models.CharField(max_length = 20, primary_key = True)
    station_description = models.TextField()
    cost_center_no_fk = models.ForeignKey(Cost_center)

    def __str__(self):
        return self.station_description

class Product(models.Model):
    nsn = models.CharField(max_length=10)
    pr_num = models.CharField(max_length=10)
    slc_num = models.IntegerField()
    inv_station_no_fk = models.ForeignKey(Inventory_stat)
    cost_center_no_fk = models.ForeignKey(Cost_center)
    item_name = models.TextField()
    generic_name = models.TextField()
    brand = models.TextField()
    part_num = models.CharField(max_length=8)
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    class_n = models.CharField(max_length=30)
    stock = models.CharField(max_length=20)
    block = models.CharField(max_length=20)
    unit_measure = models.CharField(max_length=20)
    unit_cost = models.FloatField()
    quantity = models.FloatField()
    average_amt = models.FloatField()
    status = models.CharField(max_length=20)
    balance_limit = models.FloatField()
    serial_number = models.CharField(max_length=30)
    model = models.TextField()
    amount = models.FloatField()
    description = models.TextField()
    remark = models.TextField()
    purchased_from = models.ForeignKey(Supplier)

    def __str__(self):
        return self.item_name + " , " + self.description

class Employee(models.Model):
    dce = models.CharField(max_length=8, primary_key = True)
    name = models.TextField()
    cost_center_no_fk = models.ForeignKey(Cost_center)
    charging_cc_no = models.CharField(max_length=20)
    position = models.TextField()

    def __str__(self):
        return self.dce

class Customer(models.Model):
    dce_fk = models.ForeignKey(Employee)
    credit_limit = models.FloatField()
    debit_amt = models.FloatField()
    credit_amt = models.FloatField()
    balance_amt = models.FloatField()

    def __str__(self):
        return self.dce

class IRR_header(models.Model):
    irr_headkey = models.CharField(max_length=30)
    inv_station_no = models.ForeignKey(Inventory_stat)
    reference = models.CharField(max_length=20)
    invoice_num = models.CharField(max_length=20)
    po_num = models.CharField(max_length=20)
    dr_num = models.CharField(max_length=20)
    dce_custodian = models.ForeignKey(Employee, related_name='dce1')
    dce_user = models.ForeignKey(Employee, related_name='dce2')
    proc_date = models.DateField()
    type_n = models.CharField(max_length=20)
    remark = models.TextField(max_length=100)
    date_dlvrd = models.DateField()
    supl_fk = models.ForeignKey(Supplier)

    def __str__(self):
        return self.irr_headkey

class IRR(models.Model):
    irr_no_fk = models.ForeignKey(IRR_header)
    asset_code_fk = models.ForeignKey(Product, primary_key=True)
    cost_center_no_fk = models.ForeignKey(Cost_center)
    quantity_actual = models.FloatField()
    quantity_accepted = models.FloatField()
    quantity_rejected = models.FloatField()
    quantity_balance = models.FloatField()
    date_recv = models.DateField(blank = True, null = True)
    wo_no = models.CharField(max_length=7)
    remark = models.TextField()

    def __unicode__(self):
        return str(self.irr_no_fk)

class MIV(models.Model):
    irr_no_fk = models.ForeignKey(IRR_header)
    inv_station_no_fk = models.ForeignKey(Inventory_stat)
    asset_code_fk = models.ForeignKey(Product)
    cost_center_no_fk = models.ForeignKey(Cost_center)
    wrs_num = models.CharField(max_length = 8)
    cost_center_no_fk = models.ForeignKey(Cost_center)
    quantity = models.FloatField()
    amount = models.FloatField()
    date_issued = models.DateField(blank = True, null = True)
    doc_date = models.DateField(blank = True, null = True)
    remark = models.TextField()


    def __str__(self):
        return str(self.irr_no_fk) + ", " + str(self.asset_code_fk)

class PAR(models.Model):
    dce_FK = models.ForeignKey(Employee)
    asset_code_FK = models.ForeignKey(Product)
    par_date = models.DateField(blank=True, null=True)
    par_no = models.CharField(max_length=50, null=True)
    amt_cost = models.FloatField()
    remark = models.TextField()
    qty = models.IntegerField()
    approved_by = models.ForeignKey(Employee, related_name='dce_FK2')
    issued_by = models.ForeignKey(Employee, related_name='dce_FK3')
    inv_stat_no = models.ForeignKey(Inventory_stat)
    PO_num = models.ForeignKey(IRR_header)
    date_acquired = models.DateField(blank=True, null=True)
    wo_num = models.ForeignKey(IRR)


    class Meta:
        unique_together = (("dce_FK", "asset_code_FK"))

    def __str__(self):
        return par_no

class GARV(models.Model):
    dce_FK = models.ForeignKey(Employee)
    asset_code_FK = models.ForeignKey(Product)
    garv_date = models.DateField(blank=True, null=True)
    garv_no = models.CharField(max_length=50, null=True)
    cc_num = models.ForeignKey(Cost_center)
    wo_num = models.ForeignKey(IRR)
    qty = models.CharField(max_length=50, null=True)
    par_num = models.ForeignKey(PAR)
    remarks = models.CharField(max_length=100, null=True)
    inspected_by = models.ForeignKey(Employee, related_name='dce_FK4')
    date_inspected = models.DateField(blank=True, null=True)
    confirmed_by = models.ForeignKey(Employee, related_name='dce_FK5')
    date_confirmed = models.DateField(blank=True, null=True)
    noted_by = models.ForeignKey(Employee, related_name='dce_FK6')

    class Meta:
        unique_together = ('dce_FK', 'asset_code_FK')

    def __str__(self):
        return self.dce_FK + "," + self.asset_code_FK

class Pending(models.Model):
    item_name = models.TextField()
    supplier_num = models.ForeignKey(Supplier)
    serial_number = models.CharField(max_length=50)
    model = models.TextField()
    amount = models.FloatField()
    description = models.TextField()

    class Meta:
        unique_together = ('supplier_num', 'serial_number', 'model')

    def __str__(self):
        return self.supplier_num + "," + self.serial_number + "," + self.model
