from django.shortcuts import render
from .models import *

# Create your views here.
def wrs_form(request):
    return render(request, 'WISH/wrs_form.html', {})

def par_form(request):
    return render(request, 'WISH/par_form.html', {})
    
def cme_form(request):
    return render(request, 'WISH/cme_form.html', {})

def get_all_par(request):
    par_dis = PAR.object.all()
    return render(request, 'WISH/par_form.html', {'par_dis': par_dis})

def irr_form(request):
    irrs = IRR_header.objects.all()
    suppliers = Supplier.objects.all()
    employees = Employee.objects.all()
    return render(request, 'WISH/irr_form.html', {'irrs':irrs , 'suppliers':suppliers, 'employees':employees})

def gatepass_form(request):
    return render(request, 'WISH/gatepass_form.html', {})

def miv_form(request):
    return render(request, 'WISH/miv_form.html', {})

