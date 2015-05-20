""" Register your models here."""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from WISH.models import Supplier, Product, PAR, GARV, Cost_center, \
		Inventory_stat, Employee, IRR_header, IRR, MIV



admin.site.register(Supplier, SimpleHistoryAdmin)
admin.site.register(Product, SimpleHistoryAdmin)
admin.site.register(PAR, SimpleHistoryAdmin)
admin.site.register(GARV, SimpleHistoryAdmin)
admin.site.register(Cost_center, SimpleHistoryAdmin)
admin.site.register(Inventory_stat, SimpleHistoryAdmin)
admin.site.register(Employee, SimpleHistoryAdmin)
admin.site.register(IRR_header, SimpleHistoryAdmin)
admin.site.register(IRR, SimpleHistoryAdmin)
admin.site.register(MIV, SimpleHistoryAdmin)
