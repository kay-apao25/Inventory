from django.shortcuts import render
from .models import *

# Create your views here.
def wrs_form(request):
    return render(request, 'WISH/wrs_form.html', {})

def get_all_par(request):
    par_dis = PAR.object.all()
    return render(request, 'WISH/par_form.html', {'par_dis': par_dis})

def irr_forms(request):
    return render(request, 'WISH/irr_form.html', {})

def gatepass_form(request):
    return render(request, 'WISH/gatepass_form.html', {})

def miv_form(request):
    return render(request, 'WISH/miv_form.html', {})
