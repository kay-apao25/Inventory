from django.db import models
from django.db.models.fields import CharField
from simple_history.models import HistoricalRecords
from json_field import JSONField

# Create your models here.
class Supplier(models.Model):
    supplier_number = models.CharField(max_length=15)
    supplier_name = models.TextField(max_length=20)
    supplier_address = models.TextField(max_length=20)
    telephone_number = models.CharField(max_length=20)
    credit_limit = models.FloatField()
    debit_amount = models.FloatField()
    credit_amount = models.FloatField()
    balance_amount = models.FloatField()
    contact_person = models.TextField(max_length=20)
    remarks = models.TextField(max_length=20)
    history = HistoricalRecords()

    def __str__(self):
        return self.supplier_name + ", " + self.supplier_address

class Cost_center(models.Model):
    cost_center_name = models.TextField(max_length=20)
    functional_group = models.CharField(max_length=20)
    history = HistoricalRecords()

    def __str__(self):
        return self.cost_center_name

class Inventory_stat(models.Model):
    inv_station_no = models.CharField(max_length = 20)
    station_description = models.TextField()
    cost_center_no = models.ForeignKey(Cost_center, related_name="cc_iFK")
    history = HistoricalRecords()

    def __str__(self):
        return self.station_description


class Employee(models.Model):
    dce = models.CharField(max_length=8, primary_key = True)
    name = models.TextField()
    cost_center_no = models.ForeignKey(Cost_center, related_name="cc_eFK")
    charging_cc_no = models.CharField(max_length=20)
    position = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return self.name

class Customer(models.Model):
    dce = models.ForeignKey(Employee, related_name="d_cFK")
    credit_limit = models.FloatField()
    debit_amount = models.FloatField()
    credit_amount = models.FloatField()
    balance_amount = models.FloatField()
    history = HistoricalRecords()

    def __str__(self):
        return self.dce

class Product(models.Model):
    nsn = models.CharField(max_length=10)
    slc_number = models.CharField(max_length=10)
    product_number = models.CharField(max_length=10)
    generic_name = models.TextField(max_length=25)
    item_name = models.CharField(max_length=10)
    brand = models.TextField(max_length=25)
    part_number = models.CharField(max_length=8)
    manufacture_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    unit_cost = models.FloatField()
    quantity = models.IntegerField(default = 1)
    classification = models.CharField(max_length=30)
    stock = models.CharField(max_length=10)
    block = models.CharField(max_length=10)
    unit_measure = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    purchased_from = models.ForeignKey(Supplier, related_name="s_pFK")
    average_amount = models.FloatField()
    balance_limit = models.FloatField()
    serial_number = models.CharField(max_length=15, null=True, blank=True)
    model = models.TextField(max_length=25)
    amount = models.FloatField()
    description = models.TextField(max_length=25)
    remarks = models.TextField(max_length=25, null=True, blank=True)
    history = HistoricalRecords()
    inv_station_no = models.ForeignKey(Inventory_stat, related_name="inv_iFK")
    balance = models.IntegerField(default = 0, null=True, blank=True)
    is_irr = models.BooleanField(default=False)

    def __str__(self):
        return self.item_name + " , " + self.description


class IRR_header(models.Model):
    inv_station_no = models.ForeignKey(Inventory_stat, related_name="is_iFK")
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
    supplier = models.ForeignKey(Supplier, related_name="s_iFK")
    history = HistoricalRecords()

    def __str__(self):
        return str(self.id)

class IRR(models.Model):
    product = JSONField()
    irr_headkey = models.ForeignKey(IRR_header, related_name="ih_iFK")
    irr_no = models.CharField(max_length=10, primary_key=True)
    cost_center_no = models.ForeignKey(Cost_center, null=True, blank=True, related_name="ccn_iFK")
    date_recv = models.DateField(null=True, blank=True)
    wo_no = models.CharField(max_length=7, null=True, blank=True)
    wrs_number = models.CharField(max_length = 8)
    remarks = models.TextField(max_length = 30, null=True, blank=True)
    is_par = models.BooleanField(default=False)
    is_miv = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __unicode__(self):
        return str(self.irr_no)

class MIV(models.Model):
    miv_no = models.CharField(max_length=10)
    irr_no = models.ForeignKey(IRR, related_name="i_mFK")
    wrs_number = models.CharField(max_length = 10)
    date_issued = models.DateField()
    doc_date = models.DateField()
    remarks = models.TextField(null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.irr_no)

class PAR(models.Model):
    product = JSONField()
    dce = models.ForeignKey(Employee, null=True, blank=True, related_name="d_pFK")
    par_date = models.DateField()
    par_no = models.CharField(max_length=10, primary_key=True)
    amt_cost = models.FloatField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    approved_by = models.ForeignKey(Employee, related_name='dce_FK2', null=True, blank=True)
    issued_by = models.ForeignKey(Employee, related_name='dce_FK3', null=True, blank=True)
    inv_stat_no = models.ForeignKey(Inventory_stat, related_name="is_pFK", null=True, blank=True)
    #PO_number = models.CharField(null=True, blank=True)
    date_acquired = models.DateField(null=True, blank=True)
    wo_number = models.ForeignKey(IRR, related_name="wo_pFK", null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.par_no

class GARV(models.Model):
    product_to_GARV = JSONField()
    dce = models.ForeignKey(Employee, null=True, blank=True, related_name="d_gFK")
    garv_date = models.DateField(null=True, blank=True)
    garv_no = models.CharField(max_length=10, primary_key=True)
    cc_number = models.ForeignKey(Cost_center, null=True, blank=True, related_name="cc_gFK")
    wo_number = models.ForeignKey(IRR, null=True, blank=True, related_name="wo_gFK")
    inspected_by = models.ForeignKey(Employee, related_name='dce_FK4', null=True, blank=True)
    date_inspected = models.DateField(null=True, blank=True)
    confirmed_by = models.ForeignKey(Employee, related_name='dce_FK5', null=True, blank=True)
    date_confirmed = models.DateField(null=True, blank=True)
    noted_by = models.ForeignKey(Employee, related_name='dce_FK6', null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.dce)

"""class Pending(models.Model):
    item_name = models.TextField()
    supplier_number = models.ForeignKey(Supplier, related_name="sn_penFK")
    serial_number = models.CharField(max_length=10)
    model = models.TextField()
    amount = models.FloatField()
    description = models.TextField()
    history = HistoricalRecords()

    class Meta:
        unique_together = ('supplier_number', 'serial_number', 'model')

    def __str__(self):
        return self.supplier_number + "," + self.serial_number + "," + self.model

class Try(models.Model):
    text = models.ManyToManyField(PAR)
    history = HistoricalRecords()"""
