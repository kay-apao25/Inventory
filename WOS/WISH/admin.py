from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(PAR)
admin.site.register(GARV)
admin.site.register(Pending)
admin.site.register(Cost_center)
admin.site.register(Inventory_stat)
admin.site.register(Employee)
admin.site.register(IRR_header)
admin.site.register(IRR)
admin.site.register(MIV)
admin.site.register(Product_to_IRR)
admin.site.register(Product_to_PAR)
