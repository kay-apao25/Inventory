from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.wrs_form),
    url(r'^$', views.par_form),
    url(r'^$', views.cme_form),
]