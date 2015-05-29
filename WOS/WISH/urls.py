"""urls"""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from . import views
from . import models
from . import cviews

urlpatterns = [
    url(r'^$', login_required(views.index), name='index'),
    url(r'^Aboutus/$', login_required(views.aboutus), name='aboutus'),

    #URL patterns for Log In and Out (start)
    url(r'^log_in/$', views.log_in, name='login'),
    url(r'^logout/$', login_required(views.log_out), \
        name='logout'),
    url(r'^guest/(?P<user>.*)/$', views.guest, name='guest'),
    #URL patterns for Log In and Out (end)

    #URL patterns for File and Product Fill-Up Forms (start)
    url(r'^product/new/$', login_required(views.product_new), \
    name='new_product'),
    url(r'^par/(?P<inv>[0-9]+)/$', login_required(views.par), name='new_par'),
    url(r'^par_f/$', login_required(cviews.ParF.as_view()), name='new_par_s'),
    url(r'^irr_entry/$', login_required(views.irr_entry), name='new_irr'),
    url(r'^miv_entry_f/$', login_required(cviews.MivF.as_view()),\
     name='new_miv'),
    url(r'^miv_entry/(?P<pk>[0-9]+)/$', login_required(views.miv_entry), \
        name='new_miv_s'),
    url(r'^garv_entry_f/(?P<user>.*)/$', cviews.GarvF.as_view(), \
    name='new_garv_s'),
    url(r'^garv_entry_f/$', login_required(cviews.GarvF.as_view()), \
    name='new_garv_s'),
    url(r'^product_to_garv/(?P<pk>[0-9]+)/$', views.\
        product_to_garv, name='new_garv'),
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
    url(r'^inv_stat_form/(?P<pk>[0-9]+)/$', \
    login_required(cviews.InvStatEntry.as_view()),\
     name='invstat_entry'),
    url(r'^cost_center_form/(?P<pk>[0-9]+)/$', \
    login_required(cviews.CostCenEntry.as_view()), \
        name='costcen_entry'),
    url(r'^supplier_form/(?P<pk>[0-9]+)/$', \
    login_required(views.supplier_form),\
        name='supplier_entry'),
    url(r'^employee_form/(?P<pk>[0-9]+)/$', \
    login_required(cviews.EmpEntry.as_view()), name='emp_entry'),
    #URL patterns for Editing Libraries (end)

    #URL patterns for Library Details (start)
    url(r'^product_details/(?P<pk>[0-9]+)/$', \
    login_required(cviews.ProdDetails.as_view()),\
     name='prod_details'),
    url(r'^inv_stat_details/(?P<pk>[0-9]+)/$', \
    login_required(cviews.InvStatDetails.as_view()),\
        name='invstat_details'),
    url(r'^cost_center_details/(?P<pk>[0-9]+)/$',\
     login_required(cviews.CCDetails.as_view()), \
        name='costcen_details'),
    url(r'^supplier_details/(?P<pk>[0-9]+)/$',\
     login_required(cviews.SupDetails.as_view()),\
        name='supplier_details'),
    url(r'^employee_details/(?P<pk>[0-9]+)/$', \
    login_required(cviews.EmpDetails.as_view()),\
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
    url(r'^add_cost_center/$', login_required(cviews.AddCC.as_view()), \
    name='add_cost_center'),
    url(r'^add_inv_stat/$', login_required(cviews.AddInvStat.as_view()),\
     name='add_inv_stat'),
    url(r'^add_supplier/$', views.add_supplier, name='add_supplier'),
    url(r'^add_employee/$', login_required(cviews.AddEmp.as_view()),\
     name='add_employee'),
    #URL patterns for Adding Libraries (end)

    #URL patterns for File and Product Reports (start)
    url(r'^irr_reports/$', login_required(cviews.IRRRep.as_view()),\
     name='irr_reports'),
    url(r'^miv_reports/$', login_required(cviews.MIVRep.as_view()),\
     name='miv_reports'),
    url(r'^wrs_reports/$', login_required(cviews.WRSRep.as_view()),\
     name='wrs_reports'),
    url(r'^wrs_reports/(?P<user>.*)$', cviews.WRSRep1.as_view(),\
     name='wrs_reports1'),
    url(r'^par_reports/$', login_required(cviews.PARRep.as_view()),\
     name='par_reports'),
    url(r'^garv_reports/$', login_required(cviews.GARVRep.as_view()),\
     name='garv_reports'),
    url(r'^garv_reports/(?P<user>.*)$', cviews.GARVRep1.as_view(),\
     name='garv_reports1'),
    url(r'^product_reports/$', login_required(cviews.ProdRep.as_view()),\
     name='product_reports'),
    #for guest (start)
    url(r'^wrs_entry/(?P<user>.*)/$', views.wrs_entry, name='wrs_entry'),
    #for guest (end)
    #URL patterns for File and Product Reports (end)

    #URL patterns for Viewing Libraries (start)
    url(r'^inv_stat/$', login_required(cviews.InvStatRep.as_view()),\
     name='inv_stat'),
    url(r'^cost_center/$', login_required(cviews.CCRep.as_view()),\
     name='cost_center'),
    url(r'^supplier/$', login_required(cviews.SupRep.as_view()),\
     name='supplier'),
    url(r'^employee/$', login_required(cviews.EmpRep.as_view()),\
     name='employee'),

    #URL patterns for view restore libraries
    url(r'^inv_stat_res/$', login_required(cviews.InvStatRes.as_view()),\
     name='inv_stat_res'),
    url(r'^cost_center_res/$', login_required(cviews.CCRes.as_view()),\
     name='cost_center_res'),
    url(r'^supplier_res/$', login_required(cviews.SupRes.as_view()),\
     name='supplier_res'),
    url(r'^employee_res/$', login_required(cviews.EmpRes.as_view()),\
     name='employee_res'),



    #URL patterns for details of restore libraries
    url(r'^inv_stat_details_res/(?P<pk>[0-9]+)/$', \
    login_required(cviews.InvStatDetailsRes.as_view()),\
        name='invstat_details_res'),
    url(r'^cost_center_details_res/(?P<pk>[0-9]+)/$',\
     login_required(cviews.CCDetailsRes.as_view()), \
        name='costcenter_details_res'),
    url(r'^supplier_details_res/(?P<pk>[0-9]+)/$',\
     login_required(cviews.SupDetailsRes.as_view()),\
        name='supplier_details_res'),
    url(r'^employee_details_res/(?P<pk>[0-9]+)/$', \
    login_required(cviews.EmpDetailsRes.as_view()),\
        name='emp_details_res'),

    #URL patterns for restore functionality
    url(r'^inv_stat_res/(?P<pk>[0-9]+)/$', login_required(views.inv_stat_res),\
        name='invstat_res'),
    url(r'^cost_center_res/(?P<pk>[0-9]+)/$', login_required(views.cost_center_res),\
        name='costcenter_res'),
    url(r'^supplier_res/(?P<pk>[0-9]+)/$', login_required(views.supplier_res),\
        name='supplier_res'),
    url(r'^employee_res/(?P<pk>[0-9]+)/$', login_required(views.employee_res),\
        name='employee_res'),

    #URL patterns for Viewing Libraries (end)
    url(r'^handson/$', login_required(views.handson),\
        name='handson'),
    url(r'^create_post/$', login_required(views.create_post),\
        name='create_post'),
    url(r'^my_view/$', login_required(views.my_view),\
        name='my_view'),

]
