from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'WISH/index.html', {})

def product_new(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
        result = redirect('WISH.views.index')
    else:
        form = ProductForm()
        result = render(request, 'WISH/product_add.html', {'form': form})
    return result

def irr_entry():
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
        result = redirect('WISH.views.index')
    else:
        irr_entries = IRR_entry()
        result = render(request, 'WISH/irr_entry.html', {'irr_entries': irr_entries})
    return result


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

def get_all_par(request):
    par_dis = PAR.object.all()
    return render(request, 'WISH/par_form.html', {'par_dis': par_dis})
def irr_form(request):
    irrs = IRR_header.objects.all()
    irs = IRR.objects.all()
    return render(request, 'WISH/irr_form.html', {'irrs':irrs , 'irs':irs})

def gatepass_form(request):
    return render(request, 'WISH/gatepass_form.html', {})

def miv_form(request):
    mivs = MIV.objects.all()
    return render(request, 'WISH/miv_form.html', {'mivs':mivs})

