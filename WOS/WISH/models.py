from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Supplier(models.Model):
    supplier_num = models.CharField(max_length=8)
    supplier_name = models.TextField(max_length=50)
    supplier_address = models.TextField(max_length=50)
    telephone_number = models.CharField(max_length=20)
    credit_limit = models.FloatField(max_value=None, min_value=None)
    debit_amt = models.FloatField(max_value=None, min_value=None)
    credit_amt = models.FloatField(max_value=None, min_value=None)
    balance_amt = models.FloatField(max_value=None, min_value=None)
    contact_person = models.TextField(max_length=50)
    remarks = models.TextField(max_length=100) 

	def __str__(self):
        return self.supplier_name + ", " + self.supplier_address + ", " self.supplier_num

class Product(models.Model):
    nsn = models.CharField(max_length=10) 
    slc_num = models.IntegerField() 
    inv_station_no_fk = models.ForeignKey(Inventory_stat, db_column=inv_station_no)
    cost_center_no_fk = models.ForeignKey(Cost_center, db_column=cost_center_no) 
    item_name = models.TextField(max_length=80)
    generic_name = models.TextField(max_length=100)
    brand = models.TextField(max_length=50)
    part_num = models.CharField(max_length=8)
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    class_n = models.CharField(max_length=30)
    stock = models.CharField(max_length=20)
    block = models.CharField(max_length=20)
    unit_measure = models.CharField(max_length=20)
    unit_cost = models.FloatField(max_value=None, min_value=None)
    quantity = models.FloatField(max_value=None, min_value=None)
    average_amt = models.FloatField(max_value=None, min_value=None)
    status = models.CharField(max_length=20)
    balance_limit = models.FloatField(max_value=None, min_value=None)
    serial_number = models.CharField(max_length=30)
    model = models.TextField(max_length=50)
    amount = models.FloatField(max_value=None, min_value=None)
    description = models.TextField(max_length=50)
    remark = models.TextField(max_length=100)

    def __str__(self):
        #return self.supplier_name + ", " + self.supplier_address + ", " self.supplier_num

class IRR_header(models.Model):
    irr_headkey = models.CharField(max_length=30)
    inv_station_no = models.CharField(max_length=20)
    reference = models.CharField(max_length=20)
    invoice_num = models.CharField(max_length=20)
    po_num = models.CharField(max_length=20)
    dr_num = models.CharField(max_length=20)
    dce_custodian = models.ForeignKey(Employee, db_column=dce)
    dce_user = models.ForeignKey(Employee, db_column=dce)
    proc_date = models.DateField()
    type_n = models.CharField(max_length=20)
    remark = models.TextField(max_length=100)

    def __str__(self):
        #return self.supplier_name + ", " + self.supplier_address + ", " self.supplier_num

class Cost_center(models.Model):
    cost_center_name = models.TextField(max_length=50)
    functional_group = models.CharField(max_length=30)

    def __str__(self):
        return self.cost_center_name + ", " + self.functional_group



    
