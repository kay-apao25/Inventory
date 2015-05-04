from django.db import models
#from djangotoolbox.fields import DictField
#from djorm_pgarray.fields import ArrayField
#from django.dbarray import ArrayField
#from django.contrib.postgres.fields import ArrayField
from django.db.models.fields import CharField
from simple_history.models import HistoricalRecords
from json_field import JSONField #from django_pg import models
#import dbarray
#from audit_log.models import AuthStampedModel
#from django_extensions.db.models import TimeStampedModel
#from audit_log.models.managers import AuditLog


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
    history = HistoricalRecords()

    def __str__(self):
        return self.supplier_name + ", " + self.supplier_address + ", " + self.supplier_number

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
    purchased_from = models.ForeignKey(Supplier, related_name="s_pFK")
    average_amount = models.FloatField()
    balance_limit = models.FloatField()
    serial_number = models.CharField(max_length=15)
    model = models.TextField()
    amount = models.FloatField()
    description = models.TextField()
    remark = models.TextField()
    history = HistoricalRecords()


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
    irr_no = models.IntegerField(primary_key = True)
    cost_center_no = models.ForeignKey(Cost_center, null=True, blank=True, related_name="ccn_iFK")
    date_recv = models.DateField(null=True, blank=True)
    wo_no = models.CharField(max_length=7, null=True, blank=True)
    wrs_number = models.CharField(max_length = 8)
    remark = models.TextField(max_length = 30, null=True, blank=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return str(self.irr_no)


class Product_to_IRR(models.Model):
    product = models.ForeignKey(Product, related_name="p_piFK")
    irr_no = models.ForeignKey(IRR, related_name="i_piFK")
    quantity_accepted = models.FloatField()
    quantity_rejected = models.FloatField()
    quantity_balance = models.FloatField()
    history = HistoricalRecords()

    def __str__(self):
        return str(self.product.product_number)

class MIV(models.Model):
    inv_station_no = models.ForeignKey(Inventory_stat, related_name="is_mFK")
    irr_no = models.ForeignKey(IRR, related_name="i_mFK")
    wrs_number = models.CharField(max_length = 8)
    date_issued = models.DateField()
    doc_date = models.DateField()
    remark = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return str(self.irr_no)

class PAR(models.Model):
    dce = models.ForeignKey(Employee, null=True, blank=True, related_name="d_pFK")
    par_date = models.DateField()
    par_no = models.CharField(max_length=10, primary_key=True)
    amt_cost = models.FloatField(null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    approved_by = models.ForeignKey(Employee, related_name='dce_FK2', null=True, blank=True)
    issued_by = models.ForeignKey(Employee, related_name='dce_FK3', null=True, blank=True)
    inv_stat_no = models.ForeignKey(Inventory_stat, related_name="is_pFK", null=True, blank=True)
    PO_number = models.ForeignKey(IRR_header, related_name="po_pFK", null=True, blank=True)
    date_acquired = models.DateField(null=True, blank=True)
    wo_number = models.ForeignKey(IRR, related_name="wo_pFK", null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.par_no

class Product_to_PAR(models.Model):
    par_no = models.ForeignKey(PAR, related_name="par_ppFK")
    product = models.ForeignKey(Product_to_IRR, related_name="p_ppFK")
    qty = models.IntegerField()
    history = HistoricalRecords()

    def __str__(self):
        return str(self.par_no)

class GARV(models.Model):
    dce = models.ForeignKey(Employee, null=True, blank=True, related_name="d_gFK")
    garv_date = models.DateField(null=True, blank=True)
    garv_no = models.CharField(max_length=10, primary_key=True)
    cc_number = models.ForeignKey(Cost_center, null=True, blank=True, related_name="cc_gFK")
    wo_number = models.ForeignKey(IRR_header, null=True, blank=True, related_name="wo_gFK")
    inspected_by = models.ForeignKey(Employee, related_name='dce_FK4', null=True, blank=True)
    date_inspected = models.DateField(null=True, blank=True)
    confirmed_by = models.ForeignKey(Employee, related_name='dce_FK5', null=True, blank=True)
    date_confirmed = models.DateField(null=True, blank=True)
    noted_by = models.ForeignKey(Employee, related_name='dce_FK6', null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.dce)

class Product_to_GARV(models.Model):
    garv = models.ForeignKey(GARV, related_name="g_pgFK")
    product = models.ForeignKey(Product_to_IRR, related_name="p_pgFK")
    qty = models.CharField(max_length=20)
    par_number = models.ForeignKey(PAR, related_name="pn_pgFK")
    remarks = models.CharField(max_length=20, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.par_number)

class Pending(models.Model):
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
    history = HistoricalRecords()