"""models"""
from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from json_field import JSONField


class Supplier(models.Model):
    """Supplier model"""
    supplier_number = models.CharField(max_length=8)
    supplier_name = models.CharField(max_length=40)
    supplier_address = models.CharField(max_length=40)
    telephone_number = models.CharField(max_length=11)
    credit_limit = models.FloatField()
    debit_amount = models.FloatField()
    credit_amount = models.FloatField()
    balance_amount = models.FloatField()
    contact_person = models.CharField(max_length=20)
    remarks = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.supplier_number + ", " + self.supplier_name

class InventoryStat(models.Model):
    """Inventory_stat models"""
    inv_station_no = models.CharField(max_length=40)
    station_description = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.station_description

class CostCenter(models.Model):
    """Cost_center models"""
    cost_center_name = models.CharField(max_length=40)
    inv_station_no = models.ForeignKey(InventoryStat, related_name="i_ccFK")
    functional_group = models.CharField(max_length=40)
    is_delete = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.cost_center_name


class Employee(models.Model):
    """Employee models"""
    dce = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=40)
    cost_center_no = models.ForeignKey(CostCenter, related_name="cc_eFK")
    charging_cc_no = models.CharField(max_length=20)
    position = models.CharField(max_length=20)
    history = HistoricalRecords()
    is_delete = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, default=1)
    """user = User.objects.create_user(username='guest',
                                 email='', id=1,
                                 password='guest')"""
    user_id = models.ForeignKey(User, default=1)

    def __str__(self):
        return self.name


class Customer(models.Model):
    """Customer models"""
    dce = models.ForeignKey(Employee, related_name="d_cFK")
    credit_limit = models.FloatField()
    debit_amount = models.FloatField()
    credit_amount = models.FloatField()
    balance_amount = models.FloatField()
    history = HistoricalRecords()

    def __str__(self):
        return self.dce


class Product(models.Model):
    """Product models"""
    nsn = models.CharField(max_length=15)
    slc_number = models.CharField(max_length=15)
    generic_name = models.CharField(max_length=40)
    item_name = models.CharField(max_length=40)
    brand = models.CharField(max_length=40)
    part_number = models.CharField(max_length=8)
    manufacture_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    unit_cost = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)
    classification = models.CharField(max_length=30)
    stock = models.CharField(max_length=10)
    block = models.CharField(max_length=10)
    unit_measure = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    purchased_from = models.ForeignKey(Supplier, related_name="s_pFK")
    average_amount = models.FloatField()
    balance_limit = models.FloatField()
    serial_number = models.CharField(max_length=25, null=True, blank=True)
    model = models.CharField(max_length=25)
    amount = models.FloatField()
    description = models.CharField(max_length=40)
    remarks = models.CharField(max_length=40, null=True, blank=True)
    history = HistoricalRecords()
    inv_station_no = models.ForeignKey(InventoryStat, related_name="inv_iFK")
    balance = models.PositiveIntegerField(default=0, null=True, blank=True)
    is_irr = models.BooleanField(default=False)

    def __str__(self):
        return self.item_name + " , " + self.description


class IRRHeader(models.Model):
    """IRR_header models"""
    inv_station_no = models.ForeignKey(InventoryStat, related_name="is_iFK")
    reference = models.CharField(max_length=20)
    invoice_number = models.CharField(max_length=20)
    po_number = models.CharField(max_length=20)
    pr_number = models.CharField(max_length=20)
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

    class Meta:
        unique_together = (("po_number", "pr_number", "supplier"),)


class IRR(models.Model):
    """IRR models"""
    product = JSONField()
    irr_headkey = models.ForeignKey(IRRHeader, related_name="ih_iFK")
    irr_no = models.CharField(max_length=10, primary_key=True)
    cost_center_no = models.ForeignKey(CostCenter, related_name="ccn_iFK")
    date_recv = models.DateField()
    wo_no = models.CharField(max_length=10)
    wrs_number = models.CharField(max_length=8)
    remarks = models.CharField(max_length=40, null=True, blank=True)
    is_par = models.BooleanField(default=False)
    is_miv = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.irr_no)



class MIV(models.Model):
    """MIV models"""
    miv_no = models.CharField(max_length=10, primary_key=True)
    irr_no = models.ForeignKey(IRR, related_name="i_mFK")
    date_issued = models.DateField()
    doc_date = models.DateField()
    remarks = models.CharField(max_length=40, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.irr_no)


class PAR(models.Model):
    """PAR models"""
    product = JSONField()
    dce = models.ForeignKey(Employee, related_name="d_pFK")
    par_date = models.DateField()
    par_no = models.CharField(max_length=10, primary_key=True)
    amt_cost = models.FloatField()
    remarks = models.CharField(max_length=40, null=True, blank=True)
    approved_by = models.ForeignKey(Employee, related_name='dce_FK2')
    issued_by = models.ForeignKey(Employee, related_name='dce_FK3')
    inv_stat_no = models.ForeignKey(InventoryStat, related_name="is_pFK")
    date_acquired = models.DateField()
    wo_number = models.PositiveIntegerField(default=0)
    is_garv = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.par_no

class GARV(models.Model):
    """GARV models"""
    product_to_GARV = JSONField()
    dce = models.ForeignKey(Employee, related_name="d_gFK")
    garv_date = models.DateField()
    garv_no = models.CharField(max_length=10, primary_key=True)
    cc_number = models.ForeignKey(CostCenter, related_name="cc_gFK")
    wo_number = models.PositiveIntegerField()
    inspected_by = models.ForeignKey(Employee, related_name='dce_FK4')
    date_inspected = models.DateField(null=True, blank=True)
    confirmed_by = models.ForeignKey(Employee, related_name='dce_FK5')
    date_confirmed = models.DateField(null=True, blank=True)
    noted_by = models.ForeignKey(Employee, related_name='dce_FK6')
    is_approved = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.garv_no)

class WRSPending(models.Model):
    """WRSPending models"""
    product = JSONField()
    inv_station_no = models.ForeignKey(InventoryStat, related_name="inv_wFK")
    cost_center_no = models.ForeignKey(CostCenter, related_name="cc_wFK")
    wrs_number = models.CharField(max_length=8)

    def __str__(self):
        return str(self.inv_station_no)
