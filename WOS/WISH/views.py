from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import *
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'WISH/index.html', {})

def product_new(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('WISH.views.irr_entry')
    else:
        form = ProductForm()
    return render(request, 'WISH/product_add.html', {'form': form})

def irr_entry(request):
    if request.method == "POST":
        form = IRR_entryForm(request.POST)
        if form.is_valid():
            irr_entry = form.save()
            return redirect('WISH.views.irr_entry_cont')
    else:
        form = IRR_entryForm()
    return render(request, 'WISH/irr_entry.html', {'form': form})


def irr_entry_cont(request):
    if request.method == "POST":
        form = IRR_entry_cont_Form(request.POST)
        if form.is_valid():
            irr_entry_cont = form.save()
            return redirect('WISH.views.miv_entry')
    else:
        form = IRR_entry_cont_Form()
    return render(request, 'WISH/irr_entry_cont.html', {'form': form})

def miv_entry(request):
    if request.method == "POST":
        form = MIV_entryForm(request.POST)
        if form.is_valid():
            miv_entry = form.save()
            return redirect('WISH.views.index')
    else:
        form = MIV_entryForm()
    return render(request, 'WISH/miv_entry.html', {'form': form})

def par_entry(request):
    if request.method == "POST":
        form = PAR_entryForm(request.POST)
        if form.is_valid():
            par_entry = form.save()
            return redirect('WISH.views.par_form')
    else:
        form = PAR_entryForm()
    return render(request, 'WISH/par_entry.html', {'form': form})

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
