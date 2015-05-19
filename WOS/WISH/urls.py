from django.conf.urls import include, url
from django.views.generic import ListView
from . import views
from . import models

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',  {'next_page': '/'}),
    url(r'^wrs_form/(?P<pk>[0-9]+)/$', views.wrs_form),
    url(r'^$', views.index),
    url(r'^Aboutus/$', views.aboutus),
    url(r'^product/new/$', views.product_new, name='product_new'),
    url(r'^par/(?P<inv>[0-9]+)/$', views.par),
    url(r'^par_f/$', views.par_f),
    url(r'^irr_entry/$', views.irr_entry, name='irr_entry'),
    url(r'^miv_entry/$', views.miv_entry, name='miv_entry'),
    url(r'^miv_entry_S/(?P<pk>[0-9]+)/$', views.miv_entry_S),
    url(r'^par_form/(?P<pk>[0-9]+)/$', views.par_form),
    url(r'^product_form/(?P<pk>[0-9]+)/$', views.product_form),
    url(r'^inv_stat_form/(?P<pk>[0-9]+)/$', views.inv_stat_form),
    url(r'^cost_center_form/(?P<pk>[0-9]+)/$', views.cost_center_form),
    url(r'^supplier_form/(?P<pk>[0-9]+)/$', views.supplier_form),
    url(r'^employee_form/(?P<dce>[0-9]+)/$', views.employee_form),
    url(r'^product_details/(?P<pk>[0-9]+)/$', views.product_details),
    url(r'^inv_stat_details/(?P<pk>[0-9]+)/$', views.inv_stat_details),
    url(r'^inv_stat_del/(?P<pk>[0-9]+)/$', views.inv_stat_del),
    url(r'^cost_center_del/(?P<pk>[0-9]+)/$', views.cost_center_del),
    url(r'^supplier_del/(?P<pk>[0-9]+)/$', views.supplier_del),
    url(r'^employee_del/(?P<pk>[0-9]+)/$', views.employee_del),
    url(r'^cost_center_details/(?P<pk>[0-9]+)/$', views.cost_center_details),
    url(r'^supplier_details/(?P<pk>[0-9]+)/$', views.supplier_details),
    url(r'^employee_details/(?P<dce>[0-9]+)/$', views.employee_details),
    url(r'^garv_entry_f/$', views.garv_entry_f),
    url(r'^product_to_garv/(?P<pk>[0-9]+)/$', views.product_to_garv),
    url(r'^garv_form/(?P<pk>[0-9]+)/$', views.garv_form),
    url(r'^wrs_entry/$', views.wrs_entry),
    url(r'^product_to_irr/(?P<pk>[0-9]+)/(?P<inv>[0-9]+)/$', views.product_to_irr),
    url(r'^irr_form/(?P<pk>[0-9]+)/$', views.irr_form),
    url(r'^miv_form/(?P<pk>[0-9]+)/$', views.miv_form),
    url(r'^add_cost_center/$', views.add_cost_center, name='add_cost_center'),
    url(r'^irr_reports/$', ListView.as_view(model=models.IRR, context_object_name='irr_list',\
        template_name='WISH/irr_reports.html'), name='irr_reports'),
    url(r'^miv_reports/$', ListView.as_view(model=models.MIV, context_object_name='miv_list',\
        template_name='WISH/miv_reports.html'), name='miv_reports'),
    url(r'^wrs_reports/$', ListView.as_view(model=models.IRR, context_object_name='wrs_list',\
        template_name='WISH/wrs_reports.html'), name='wrs_reports'),
    url(r'^par_reports/$', ListView.as_view(model=models.PAR, context_object_name='par_list',\
        template_name='WISH/par_reports.html'), name='par_reports'),
    url(r'^garv_reports/$', ListView.as_view(model=models.GARV, context_object_name='garv_list',\
        template_name='WISH/garv_reports.html'), name='garv_reports'),
    url(r'^product_reports/$', ListView.as_view(model=models.Product, context_object_name='product_list',\
        template_name='WISH/product_reports.html'), name='product_reports'),
    url(r'^inv_stat/$', ListView.as_view(model=models.Inventory_stat, context_object_name='inv_list',\
        template_name='WISH/inv_stat.html'), name='inv_stat'),
    url(r'^cost_center/$', ListView.as_view(model=models.Cost_center, context_object_name='cc_list',\
        template_name='WISH/cost_center.html'), name='cost_center'),
    url(r'^supplier/$', ListView.as_view(model=models.Supplier, context_object_name='sup_list',\
        template_name='WISH/supplier.html'), name='supplier'),
    url(r'^employee/$', ListView.as_view(model=models.Employee, context_object_name='em_list',\
        template_name='WISH/employee.html'), name='employee'),
    #url(r'^libraries/$', views.libraries),
    url(r'^stat_lib/$', views.stat_lib, name='stat_lib'),
    url(r'^sup_lib/$', views.sup_lib, name='sup_lib'),
    url(r'^employee_lib/$', views.employee_lib, name='employee_lib'),
]
