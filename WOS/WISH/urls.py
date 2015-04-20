from django.conf.urls import include, url
from . import views

urlpatterns = [
<<<<<<< HEAD
    #url(r'^$', views.wrs_form),
    #url(r'^$', views.par_form),
    #url(r'^$', views.cme_form),
=======
    url(r'^$', views.index),
    url(r'^product/new/$', views.product_new, name='product_new'),
    url(r'^$', views.wrs_form),
    url(r'^$', views.wrs_form),
    url(r'^$', views.par_form),
    url(r'^$', views.cme_form),
>>>>>>> 7e16b3fb9b057b6c9e410a37d1e068f5b2cc4b3a
    url(r'^$', views.irr_form),
    #url(r'^$', views.gatepass_form),
    #url(r'^$', views.miv_form),
]