from django.shortcuts import render
from .models import *

# Create your views here.
def wrs_form(request):
    return render(request, 'WISH/wrs_form.html', {})

def par_form(request):
    pars = PAR.objects.all()
    return render(request, 'WISH/par_form.html', {'pars': pars})
    
def cme_form(request):
    return render(request, 'WISH/cme_form.html', {})

def irr_forms(request):
    return render(request, 'WISH/irr_form.html', {})

def gatepass_form(request):
    return render(request, 'WISH/gatepass_form.html', {})

def miv_form(request):
    return render(request, 'WISH/miv_form.html', {})

