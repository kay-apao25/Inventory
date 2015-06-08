""" Register your models here."""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from WISH.models import Supplier, Product, PAR, GARV, CostCenter, \
		InventoryStat, Employee, IRRHeader, IRR, MIV, Customer, WRSPending, Unit_Measure

admin.site.register(Supplier, SimpleHistoryAdmin)
admin.site.register(Product, SimpleHistoryAdmin)
admin.site.register(PAR, SimpleHistoryAdmin)
admin.site.register(GARV, SimpleHistoryAdmin)
admin.site.register(CostCenter, SimpleHistoryAdmin)
admin.site.register(InventoryStat, SimpleHistoryAdmin)
admin.site.register(Employee, SimpleHistoryAdmin)
admin.site.register(IRRHeader, SimpleHistoryAdmin)
admin.site.register(IRR, SimpleHistoryAdmin)
admin.site.register(MIV, SimpleHistoryAdmin)
admin.site.register(Customer, SimpleHistoryAdmin)
admin.site.register(WRSPending, SimpleHistoryAdmin)
admin.site.register(Unit_Measure)
