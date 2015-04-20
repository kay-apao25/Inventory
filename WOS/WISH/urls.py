from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^wrs_form/$', views.wrs_form),
    #url(r'^$', views.par_form),
    #url(r'^$', views.cme_form),
    url(r'^$', views.index),
    url(r'^product/new/$', views.product_new, name='product_new'),
    #url(r'^$', views.irr_form),
    url(r'^irr_entry/$', views.irr_entry, name='irr_entry'),
    url(r'^irr_entry_cont/$', views.irr_entry_cont, name='irr_entry_cont'),
    url(r'^par_entry/$', views.par_entry, name='par_entry'),
    #url(r'^$', views.gatepass_form),
    #url(r'^$', views.miv_form),
]
