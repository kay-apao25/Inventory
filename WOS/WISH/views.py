from django.shortcuts import render
from .models import *
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'WISH/index.html', {})

def product_new(request):
    form = ProductForm()
    return render(request, 'WISH/product_add.html', {'form': form})

def wrs_form(request):
    wrss = MIV.objects.filter(wrs_num=1)
    prods = Product.objects.all()
    i_heads = IRR_header.objects.all()
    return render(request, 'WISH/wrs_form.html', {'wrss': wrss})

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

