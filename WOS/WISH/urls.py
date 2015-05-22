"""urls"""
from django.conf.urls import url
from django.views.generic import ListView
from . import views
from . import models

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^Aboutus/$', views.aboutus, name='aboutus'),

    #URL patterns for Log In and Out (start)
    url(r'^login/$', 'django.contrib.auth.views.login', \
        name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', \
        {'next_page': '/'}, name='logout'),
    url(r'^guest/$', views.guest, name='guest'),
    #URL patterns for Log In and Out (end)

    #URL patterns for File and Product Fill-Up Forms (start)
    url(r'^product/new/$', views.product_new, name='new_product'),
    url(r'^par/(?P<inv>[0-9]+)/$', views.par, name='new_par'),
    url(r'^par_f/$', views.par_f, name='new_par_s'),
    url(r'^irr_entry/$', views.irr_entry, name='new_irr'),
    url(r'^miv_entry/$', views.miv_entry, name='new_miv'),
    url(r'^miv_entry_S/(?P<pk>[0-9]+)/$', views.miv_entry_S, \
        name='new_miv_s'),
    url(r'^garv_entry_f/$', views.garv_entry_f, name='new_garv_s'),
    url(r'^product_to_garv/(?P<pk>[0-9]+)/$', views.product_to_garv,\
        name='new_garv'),
    url(r'^wrs_entry/$', views.wrs_entry, name='wrs_entry'),
    url(r'^product_to_irr/(?P<pk>[0-9]+)/(?P<inv>[0-9]+)/$', views.\
        product_to_irr, name='new_irr_cont'),
    #URL patterns for File and Product Fill-Up Forms (end)

    #URL patterns for File Forms (start)
    url(r'^par_form/(?P<pk>[0-9]+)/$', views.par_form, name='par_form'),
    url(r'^irr_form/(?P<pk>[0-9]+)/$', views.irr_form, name='irr_form'),
    url(r'^miv_form/(?P<pk>[0-9]+)/$', views.miv_form, name='miv_form'),
    url(r'^garv_form/(?P<pk>[0-9]+)/$', views.garv_form, name='garv_form'),
    url(r'^wrs_form/(?P<pk>[0-9]+)/$', views.wrs_form, name='wrs_form'),
    #URL patterns for File Forms (end)

    #URL patterns for Editing Libraries (start)
    url(r'^product_form/(?P<pk>[0-9]+)/$', views.product_form,\
        name='product_entry'),
    url(r'^inv_stat_form/(?P<pk>[0-9]+)/$', views.inv_stat_form,\
        name='invstat_entry'),
    url(r'^cost_center_form/(?P<pk>[0-9]+)/$', \
        views.cost_center_form, name='costcen_entry'),
    url(r'^supplier_form/(?P<pk>[0-9]+)/$', views.supplier_form,\
        name='supplier_entry'),
    url(r'^employee_form/(?P<dce>[0-9]+)/$', views.employee_form,\
        name='emp_entry'),
    #URL patterns for Editing Libraries (end)

    #URL patterns for Library Details (start)
    url(r'^product_details/(?P<pk>[0-9]+)/$', views.product_details,\
        name='prod_details'),
    url(r'^inv_stat_details/(?P<pk>[0-9]+)/$', views.inv_stat_details,\
        name='invstat_details'),
    url(r'^cost_center_details/(?P<pk>[0-9]+)/$', \
        views.cost_center_details, name='costcen_details'),
    url(r'^supplier_details/(?P<pk>[0-9]+)/$', views.supplier_details,\
        name='supplier_details'),
    url(r'^employee_details/(?P<dce>[0-9]+)/$', views.employee_details,\
        name='emp_details'),
    #URL patterns for Library Details (end)

    #URL patterns for Deleting Libraries (start)
    url(r'^inv_stat_del/(?P<pk>[0-9]+)/$', views.inv_stat_del,\
        name='invstat_del'),
    url(r'^cost_center_del/(?P<pk>[0-9]+)/$', \
        views.cost_center_del, name='costcen_del'),
    url(r'^supplier_del/(?P<pk>[0-9]+)/$', views.supplier_del,\
        name='supplier_del'),
    url(r'^employee_del/(?P<pk>[0-9]+)/$', views.employee_del,\
        name='emp_del'),
    #URL patterns for Deleting Libraries (end)

    #URL patterns for Adding Libraries (start)
    url(r'^add_cost_center/$', views.add_cost_center,\
     name='add_cost_center'),
    url(r'^add_inv_stat/$', views.add_inv_stat, name='add_inv_stat'),
    url(r'^add_supplier/$', views.add_supplier, name='add_supplier'),
    url(r'^add_employee/$', views.add_employee, name='add_employee'),
    #URL patterns for Adding Libraries (end)

    #URL patterns for File and Product Reports (start)
    url(r'^irr_reports/$', lambda request: ListView.as_view(queryset=\
        models.IRR.objects.filter(irr_headkey__in=[i.id for i in (\
        models.IRRHeader.objects.filter(dce_custodian=(\
        models.Employee.objects.get(name=str(request.user.\
        first_name) + ' ' + str(request.user.last_name)))))]),
        context_object_name='irr_list', template_name=\
        'WISH/irr_reports.html')(request), name='irr_reports'),
    url(r'^miv_reports/$',lambda request: ListView.as_view(queryset=\
        models.MIV.objects.filter(irr_no=models.IRR.objects.filter(\
        irr_headkey__in=[i.id for i in (models.IRRHeader.objects.filter(\
        dce_custodian=(models.Employee.objects.get(name=str(request.user.\
        first_name) + ' ' + str(request.user.last_name)))))])),
        context_object_name='miv_list', template_name=\
        'WISH/miv_reports.html')(request), name='miv_reports'),
    url(r'^wrs_reports/$', lambda request: ListView.as_view(queryset=\
        models.IRR.objects.filter(irr_headkey__in=[i.id for i in (\
        models.IRRHeader.objects.filter(dce_custodian=(\
        models.Employee.objects.get(name=str(request.user.\
        first_name) + ' ' + str(request.user.last_name)))))]),
        context_object_name='wrs_list', template_name=\
        'WISH/wrs_reports.html')(request), name='wrs_reports'),
    url(r'^par_reports/$', lambda request: ListView.as_view(queryset=\
        models.PAR.objects.filter(issued_by=(models.Employee.objects.get(\
        name=str(request.user.first_name) + ' ' + str(request.user.last_name\
        )))), context_object_name='par_list', template_name=\
        'WISH/par_reports.html')(request), name='par_reports'),
    url(r'^garv_reports/$', lambda request: ListView.as_view(queryset=\
        models.GARV.objects.filter(confirmed_by=(models.Employee.objects.get(\
        name=str(request.user.first_name) + ' ' + str(request.user.last_name\
        )))), context_object_name='garv_list', template_name=\
        'WISH/garv_reports.html')(request), name='garv_reports'),
    url(r'^product_reports/$', lambda request: ListView.as_view(queryset=\
        models.Product.objects.filter(inv_station_no__in=[i.inv_station_no \
        for i in (models.InventoryStat.objects.filter(cost_center_no=(\
        models.Employee.objects.get(name=str(request.user.first_name) \
        + ' ' + str(request.user.last_name)).cost_center_no)))]),
        context_object_name='irr_list', template_name=\
        'WISH/product_reports.html')(request), name='product_reports'),
    #for guest (start)
    url(r'^wrs_reports1/$', lambda request: ListView.as_view(model=models.IRR,
        context_object_name='irr_list', template_name=\
        'WISH/wrs_reports1.html')(request), name='wrs_reports1'),
    #for guest (end)
    #URL patterns for File and Product Reports (end)

    #URL patterns for Viewing Libraries (start)
    url(r'^inv_stat/$', lambda request: ListView.as_view(queryset=\
        models.InventoryStat.objects.filter(is_delete=False).filter(cost_center_no_id=\
        (models.Employee.objects.get(name=str(request.user.first_name) \
        + ' ' + str(request.user.last_name)).cost_center_no_id)),
        context_object_name='inv_list', template_name='WISH/inv_stat.html')(request),
        name='inv_stat'),

    url(r'^cost_center/$', ListView.as_view(queryset=\
        models.CostCenter.objects.filter(is_delete=False),
        context_object_name='cc_list', template_name='WISH/cost_center.html'),
        name='cost_center'),

    url(r'^supplier/$', ListView.as_view(queryset=models.Supplier.objects.filter(is_delete=False), \
        context_object_name='sup_list',\
        template_name='WISH/supplier.html'), name='supplier'),

    url(r'^employee/$', lambda request: ListView.as_view(queryset=\
        models.Employee.objects.filter(is_delete=False).filter(cost_center_no_id=\
        (models.Employee.objects.get(name=str(request.user.first_name) \
        + ' ' + str(request.user.last_name)).cost_center_no_id)),
        context_object_name='em_list',\
        template_name='WISH/employee.html')(request), name='employee'),
    #URL patterns for Viewing Libraries (end)
]
