"""urls"""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy
from . import views
from . import models
from . import forms

urlpatterns = [
    url(r'^$', login_required(views.index), name='index'),
    url(r'^Aboutus/$', login_required(views.aboutus), name='aboutus'),

    #URL patterns for Log In and Out (start)
    url(r'^log_in/$', views.log_in, name='login'),
    url(r'^logout/$', login_required(views.log_out), \
        name='logout'),
    url(r'^guest/$', views.guest, name='guest'),
    #URL patterns for Log In and Out (end)

    #URL patterns for File and Product Fill-Up Forms (start)
    url(r'^product/new/$', login_required(views.product_new), name='new_product'),
    url(r'^par/(?P<inv>[0-9]+)/$', login_required(views.par), name='new_par'),
    url(r'^par_f/$', login_required(views.par_f), name='new_par_s'),
    url(r'^irr_entry/$', login_required(views.irr_entry), name='new_irr'),
    url(r'^miv_entry/$', login_required(views.miv_entry), name='new_miv'),
    url(r'^miv_entry_S/(?P<pk>[0-9]+)/$', login_required(views.miv_entry_S), \
        name='new_miv_s'),
    url(r'^garv_entry_f/$', login_required(views.garv_entry_f), name='new_garv_s'),
    url(r'^product_to_garv/(?P<pk>[0-9]+)/$', login_required(views.product_to_garv),\
        name='new_garv'),
    #url(r'^wrs_entry/$', views.wrs_entry, name='wrs_entry'),
    url(r'^product_to_irr/(?P<pk>[0-9]+)/(?P<inv>[0-9]+)/$', login_required(\
        views.product_to_irr), name='new_irr_cont'),
    #URL patterns for File and Product Fill-Up Forms (end)

    #URL patterns for File Forms (start)
    url(r'^par_form/(?P<pk>[0-9]+)/$', login_required(views.par_form), \
        name='par_form'),
    url(r'^irr_form/(?P<pk>[0-9]+)/$', login_required(views.irr_form), \
        name='irr_form'),
    url(r'^miv_form/(?P<pk>[0-9]+)/$', login_required(views.miv_form), \
        name='miv_form'),
    url(r'^garv_form/(?P<pk>[0-9]+)/$', login_required(views.garv_form), \
        name='garv_form'),
    url(r'^wrs_form/(?P<pk>[0-9]+)/$', login_required(views.wrs_form), \
        name='wrs_form'),
    #URL patterns for File Forms (end)

    #URL patterns for Editing Libraries (start)
    url(r'^product_form/(?P<pk>[0-9]+)/$', login_required(views.product_form),\
        name='product_entry'),
    url(r'^inv_stat_form/(?P<pk>[0-9]+)/$', login_required(UpdateView.as_view(\
        model=models.InventoryStat, form_class=forms.Statlib1, success_url=\
        reverse_lazy('inv_stat'))), name='invstat_entry'),
    url(r'^cost_center_form/(?P<pk>[0-9]+)/$', login_required(UpdateView.as_view(\
        model=models.CostCenter, form_class=forms.CClib, success_url=reverse_lazy(\
        'cost_center'))), name='costcen_entry'),
    url(r'^supplier_form/(?P<pk>[0-9]+)/$', login_required(views.supplier_form),\
        name='supplier_entry'),
    url(r'^employee_form/(?P<pk>[0-9]+)/$', login_required(UpdateView.as_view(\
        model=models.Employee, form_class=forms.Employeelib, success_url=\
        reverse_lazy('employee'))), name='emp_entry'),
    #URL patterns for Editing Libraries (end)

    #URL patterns for Library Details (start)
    url(r'^product_details/(?P<pk>[0-9]+)/$', login_required(DetailView.as_view(\
            model=models.Product, context_object_name='prod')), name='prod_details'),
    url(r'^inv_stat_details/(?P<pk>[0-9]+)/$', login_required(DetailView.as_view(\
            model=models.InventoryStat, context_object_name='invs')),\
        name='invstat_details'),
    url(r'^cost_center_details/(?P<pk>[0-9]+)/$', login_required(DetailView.as_view(\
            model=models.CostCenter, context_object_name='cc')), \
        name='costcen_details'),
    url(r'^supplier_details/(?P<pk>[0-9]+)/$', login_required(DetailView.as_view(\
            model=models.Supplier, context_object_name='sup')),\
        name='supplier_details'),
    url(r'^employee_details/(?P<pk>[0-9]+)/$', login_required(DetailView.as_view(\
            model=models.Employee, context_object_name='em')),\
        name='emp_details'),
    #URL patterns for Library Details (end)

    #URL patterns for Deleting Libraries (start)
    url(r'^inv_stat_del/(?P<pk>[0-9]+)/$', login_required(views.inv_stat_del),\
        name='invstat_del'),
    url(r'^cost_center_del/(?P<pk>[0-9]+)/$', \
        views.cost_center_del, name='costcen_del'),
    url(r'^supplier_del/(?P<pk>[0-9]+)/$', login_required(views.supplier_del),\
        name='supplier_del'),
    url(r'^employee_del/(?P<pk>[0-9]+)/$', login_required(views.employee_del),\
        name='emp_del'),
    #URL patterns for Deleting Libraries (end)

    #URL patterns for Adding Libraries (start)
    url(r'^add_cost_center/$', login_required(CreateView.as_view(form_class=forms.CClib, \
            template_name='WISH/add_cost_center.html', success_url=reverse_lazy(\
            'cost_center'))), name='add_cost_center'),
    url(r'^add_inv_stat/$', login_required(CreateView.as_view(form_class=forms.Statlib, \
            template_name='WISH/add_inv_stat.html', success_url=reverse_lazy(\
            'inv_stat'))), name='add_inv_stat'),
    url(r'^add_supplier/$', views.add_supplier, name='add_supplier'),
    url(r'^add_employee/$', views.add_employee, name='add_employee'),
    #URL patterns for Adding Libraries (end)

    #URL patterns for File and Product Reports (start)
    url(r'^irr_reports/$', login_required(lambda request: ListView.as_view(queryset=\
        models.IRR.objects.filter(irr_headkey__in=[i.id for i in (\
        models.IRRHeader.objects.filter(dce_custodian=(\
        models.Employee.objects.get(name=str(request.user.\
        first_name) + ' ' + str(request.user.last_name)))))]),
        context_object_name='irr_list', template_name=\
        'WISH/irr_reports.html')(request)), name='irr_reports'),

    url(r'^miv_reports/$', login_required(lambda request: ListView.as_view(queryset=\
        models.MIV.objects.filter(irr_no=models.IRR.objects.filter(\
        irr_headkey__in=[i.id for i in (models.IRRHeader.objects.filter(\
        dce_custodian=(models.Employee.objects.get(name=str(request.user.\
        first_name) + ' ' + str(request.user.last_name)))))])),
        context_object_name='miv_list', template_name=\
        'WISH/miv_reports.html')(request)), name='miv_reports'),
    url(r'^wrs_reports/$', login_required(lambda request: ListView.as_view(queryset=\
        models.IRR.objects.filter(irr_headkey__in=[i.id for i in (\
        models.IRRHeader.objects.filter(dce_custodian=(\
        models.Employee.objects.get(name=str(request.user.\
        first_name) + ' ' + str(request.user.last_name)))))]),
        context_object_name='wrs_list', template_name=\
        'WISH/wrs_reports.html')(request)), name='wrs_reports'),

    url(r'^par_reports/$', login_required(lambda request: ListView.as_view(queryset=\
        models.PAR.objects.filter(issued_by=(models.Employee.objects.get(\
        name=str(request.user.first_name) + ' ' + str(request.user.last_name\
        )))), context_object_name='par_list', template_name=\
        'WISH/par_reports.html')(request)), name='par_reports'),

    url(r'^garv_reports/$', login_required(lambda request: ListView.as_view(queryset=\
        models.GARV.objects.filter(confirmed_by=(models.Employee.objects.get(\
        name=str(request.user.first_name) + ' ' + str(request.user.last_name\
        )))), context_object_name='garv_list', template_name=\
        'WISH/garv_reports.html')(request)), name='garv_reports'),

    url(r'^product_reports/$', login_required(lambda request: ListView.as_view(queryset=\
        models.Product.objects.filter(inv_station_no__in=[i.inv_station_no \
        for i in (models.InventoryStat.objects.filter(cost_center_no=(\
        models.Employee.objects.get(name=str(request.user.first_name) \
        + ' ' + str(request.user.last_name)).cost_center_no)))]),
        context_object_name='product_list', template_name=\
        'WISH/product_reports.html')(request)), name='product_reports'),
    #for guest (start)
    url(r'^wrs_reports1/$', lambda request: ListView.as_view(model=models.IRR,
        context_object_name='irr_list', template_name=\
        'WISH/wrs_reports1.html')(request), name='wrs_reports1'),
    #for guest (end)
    #URL patterns for File and Product Reports (end)

    #URL patterns for Viewing Libraries (start)
    url(r'^inv_stat/$', login_required(lambda request: ListView.as_view(queryset=\
            models.InventoryStat.objects.filter(is_delete=False).filter(cost_center_no_id=\
            (models.Employee.objects.get(name=str(request.user.first_name) \
            + ' ' + str(request.user.last_name)).cost_center_no_id)),
            context_object_name='inv_list', template_name='WISH/inv_stat.html')(request)),
        name='inv_stat'),

    url(r'^cost_center/$', login_required(ListView.as_view(queryset=\
        models.CostCenter.objects.filter(is_delete=False), context_object_name=\
        'cc_list', template_name='WISH/cost_center.html')), name='cost_center'),

    url(r'^supplier/$', login_required(ListView.as_view(queryset=\
        models.Supplier.objects.filter(is_delete=False), context_object_name='sup_list',\
        template_name='WISH/supplier.html')), name='supplier'),

    url(r'^employee/$', login_required(lambda request: ListView.as_view(queryset=\
        models.Employee.objects.filter(is_delete=False).filter(cost_center_no_id=\
        (models.Employee.objects.get(name=str(request.user.first_name) \
        + ' ' + str(request.user.last_name)).cost_center_no_id)),
        context_object_name='em_list',\
        template_name='WISH/employee.html')(request)), name='employee'),
    #URL patterns for Viewing Libraries (end)
]
