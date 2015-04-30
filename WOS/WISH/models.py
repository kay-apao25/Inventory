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
    inv_station_no = models.CharField(max_length = 20)
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

class Product(models.Model):
    nsn = models.CharField(max_length=10)
    slc_number = models.IntegerField()
    product_number = models.CharField(max_length=10)
    generic_name = models.TextField()
    item_name = models.CharField(max_length=10)
    brand = models.TextField()
    part_number = models.CharField(max_length=8)
    manufacture_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    unit_cost = models.FloatField()
    quantity = models.FloatField(default = '1')
    classification = models.CharField(max_length=30)
    stock = models.CharField(max_length=10)
    block = models.CharField(max_length=10)
    unit_measure = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    purchased_from = models.ForeignKey(Supplier)
    average_amount = models.FloatField()
    balance_limit = models.FloatField()
    serial_number = models.CharField(max_length=15)
    model = models.TextField()
    amount = models.FloatField()
    description = models.TextField()
    remark = models.TextField()


    def __str__(self):
        return self.item_name + " , " + self.description


class IRR_header(models.Model):
    inv_station_no = models.ForeignKey(Inventory_stat)
    reference = models.CharField(max_length=20)
    invoice_number = models.CharField(max_length=20)
    po_number = models.CharField(max_length=20)
    dr_number = models.CharField(max_length=20)
    dce_custodian = models.ForeignKey(Employee, related_name='dce1')
    dce_user = models.ForeignKey(Employee, related_name='dce2')
    dce_approved = models.ForeignKey(Employee, related_name='dce3')
    proc_date = models.DateField()
    approved_date = models.DateField()
    type_n = models.CharField(max_length=20)
    date_dlvrd = models.DateField()
    supplier = models.ForeignKey(Supplier)

    def __str__(self):
        return str(self.id)

class IRR(models.Model):
    irr_headkey = models.ForeignKey(IRR_header)
    irr_no = models.IntegerField(primary_key = True)
    cost_center_no = models.ForeignKey(Cost_center, null=True, blank=True)
    date_recv = models.DateField(null=True, blank=True)
    wo_no = models.CharField(max_length=7, null=True, blank=True)
    remark = models.TextField(max_length = 30, null=True, blank=True)

    def __unicode__(self):
        return str(self.irr_no)


class Product_to_IRR(models.Model):
    product = models.ForeignKey(Product)
    irr_no = models.ForeignKey(IRR)
    quantity_accepted = models.FloatField()
    quantity_rejected = models.FloatField()
    quantity_balance = models.FloatField()

    def __str__(self):
        return str(self.product.product_number)

class MIV(models.Model):
    inv_station_no = models.ForeignKey(Inventory_stat)
    irr_no = models.ForeignKey(IRR)
    wrs_number = models.CharField(max_length = 8)
    date_issued = models.DateField()
    doc_date = models.DateField()
    remark = models.TextField()

    def __str__(self):
        return str(self.irr_no)

class PAR(models.Model):
    dce = models.ForeignKey(Employee, null=True, blank=True)
    par_date = models.DateField()
    par_no = models.CharField(max_length=10)
    amt_cost = models.FloatField(null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    approved_by = models.ForeignKey(Employee, related_name='dce_FK2', null=True, blank=True)
    issued_by = models.ForeignKey(Employee, related_name='dce_FK3', null=True, blank=True)
    inv_stat_no = models.ForeignKey(Inventory_stat, null=True, blank=True)
    PO_number = models.ForeignKey(IRR_header, null=True, blank=True)
    date_acquired = models.DateField(null=True, blank=True)
    wo_number = models.ForeignKey(IRR, null=True, blank=True)

    def __str__(self):
        return self.par_no

class Product_to_PAR(models.Model):
    par_no = models.ForeignKey(PAR)
    product = models.ForeignKey(Product_to_IRR)
    qty = models.IntegerField()

    def __str__(self):
        return str(self.par_no)

class GARV(models.Model):
    dce = models.ForeignKey(Employee, null=True, blank=True)
    garv_date = models.DateField(null=True, blank=True)
    garv_no = models.CharField(max_length=10)
    cc_number = models.ForeignKey(Cost_center, null=True, blank=True)
    wo_number = models.ForeignKey(IRR_header, null=True, blank=True)
    inspected_by = models.ForeignKey(Employee, related_name='dce_FK4', null=True, blank=True)
    date_inspected = models.DateField(null=True, blank=True)
    confirmed_by = models.ForeignKey(Employee, related_name='dce_FK5', null=True, blank=True)
    date_confirmed = models.DateField(null=True, blank=True)
    noted_by = models.ForeignKey(Employee, related_name='dce_FK6', null=True, blank=True)

    def __str__(self):
        return str(self.dce)

class Product_to_GARV(models.Model):
    garv = models.ForeignKey(GARV)
    product = models.ForeignKey(Product_to_IRR)
    qty = models.CharField(max_length=20)
    par_number = models.ForeignKey(PAR)
    remarks = models.CharField(max_length=20, null=True)

    def __str__(self):
        return str(self.par_number)

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
