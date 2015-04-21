from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^wrs_form/$', views.wrs_form),
    #url(r'^$', views.cme_form),
    url(r'^$', views.index),
    url(r'^product/new/$', views.product_new, name='product_new'),
    url(r'^irr_miv_form/(?P<mpk>[0-9]+)/(?P<ipk>[0-9]+)$', views.irr_miv_form, name='irr_miv_form'),
    url(r'^irr_entry/$', views.irr_entry, name='irr_entry'),
    #url(r'^irr_entry_cont/$', views.irr_entry_cont, name='irr_entry_cont'),
    url(r'^miv_entry/(?P<pk>[0-9]+)/$', views.miv_entry, name='miv_entry'),
    url(r'^par_entry/$', views.par_entry, name='par_entry'),
    url(r'^par_form/$', views.par_form),
    url(r'^garv_form/$', views.garv_form),
    url(r'^product/new/(?P<pk>[0-9]+)/(?P<instat>[0-9]+)/(?P<sup>[0-9]+)/$', views.irr_entry),
    url(r'^product/new/(?P<ipk>[0-9]+)/(?P<pk>[0-9]+)/$', views.irr_entry_cont),
    #url(r'^irr_form/$', views.irr_form),
    #url(r'^$', views.gatepass_form),
    #url(r'^$', views.miv_form),
]
