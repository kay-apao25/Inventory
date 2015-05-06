from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^wrs_form/(?P<pk>[0-9]+)/$', views.wrs_form),
    #url(r'^$', views.cme_form),
    url(r'^$', views.index),
    url(r'^product/new/$', views.product_new, name='product_new'),
    url(r'^par/(?P<inv>[0-9]+)/$', views.par),
    url(r'^par_f/$', views.par_f),
    #url(r'^try/$', views.try_entry),
    #url(r'^irr_miv_form/(?P<mpk>[0-9]+)/(?P<ipk>[0-9]+)$', views.irr_miv_form, name='irr_miv_form'),
    url(r'^irr_entry/$', views.irr_entry, name='irr_entry'),
    #url(r'^irr_entry_cont/(?P<pk>[0-9]+)/$', views.irr_entry_cont, name='irr_entry_cont'),
    url(r'^miv_entry/$', views.miv_entry, name='miv_entry'),
    url(r'^miv_entry_S/(?P<pk>[0-9]+)/$', views.miv_entry_S),
    url(r'^par_entry/(?P<pk>[0-9]+)/$', views.par_entry, name='par_entry'),
    url(r'^par_form/(?P<pk>[0-9]+)/$', views.par_form),
    url(r'^product_form/(?P<pk>[0-9]+)/$', views.product_form),
    url(r'^garv_entry_f/$', views.garv_entry_f),
    url(r'^garv_entry/(?P<g>[0-9]+)/(?P<pk>[0-9]+)/$', views.garv_entry),
    url(r'^product_to_garv/(?P<pk>[0-9]+)/$', views.product_to_garv),
    url(r'^garv_form/(?P<pk>[0-9]+)/$', views.garv_form),
    url(r'^wrs_entry/$', views.wrs_entry),
    url(r'^product_to_irr/(?P<pk>[0-9]+)/(?P<irn>[0-9]+)/(?P<inv>[0-9]+)/$', views.product_to_irr),
    #url(r'^product/new/(?P<pk>[0-9]+)/(?P<instat>[0-9]+)/(?P<sup>[0-9]+)/$', views.irr_entry),
    #url(r'^product/new/(?P<ipk>[0-9]+)/(?P<pk>[0-9]+)/(?P<instat>[0-9]+)/k$', views.irr_entry_cont),
    url(r'^irr_form/(?P<pk>[0-9]+)/$', views.irr_form),
    #url(r'^$', views.gatepass_form),
    url(r'^miv_form/(?P<pk>[0-9]+)/$', views.miv_form),
    url(r'^irr_report/$', views.irr_report),
    url(r'^miv_report/$', views.miv_report),
    url(r'^par_report/$', views.par_report),
    url(r'^garv_report/$', views.garv_report),
    url(r'^file_reports/$', views.file_report),
    url(r'^irr_reports/$', views.irr_reports),
    url(r'^miv_reports/$', views.miv_reports),
    url(r'^wrs_reports/$', views.wrs_reports),
    url(r'^par_reports/$', views.par_reports),
    url(r'^garv_reports/$', views.garv_reports),
    url(r'^product_reports/$', views.product_reports),
    url(r'^file_entry/$', views.file_entry),

]
