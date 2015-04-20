from django.conf.urls import include, url
from . import views

urlpatterns = [
    #url(r'^$', views.wrs_form),
    #url(r'^$', views.par_form),
    #url(r'^$', views.cme_form),
    #url(r'^$', views.index),
    #url(r'^product/new/$', views.product_new, name='product_new'),
    url(r'^$', views.irr_form),
    #url(r'^$', views.gatepass_form),
    #url(r'^$', views.miv_form),
]