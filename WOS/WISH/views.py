from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from random import randint
from .models import *
from .forms import *
import time

# Create your views here.
def index(request):
    return render(request, 'WISH/index.html', {})

def wrs_num(request):
    return render(request, 'WISH/wrs_num.html', {})

def product_new(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.slc_num = randint(100000,999999)
            product.nsn = randint(500000,999999)  
            product.amount = product.unit_cost * product.quantity
            product.save()
            return redirect('WISH.views.irr_entry', pk=product.pk, instat=product.inv_station_no_fk_id, sup=product.purchased_from_id)
    else:
        form = ProductForm()
    return render(request, 'WISH/product_add.html', {'form': form})

def irr_entry(request, pk, instat, sup):
    if request.method == "POST":
        form = IRR_entryForm(request.POST)
        if form.is_valid():
            irr_entry = form.save(commit=False)
            irr_entry.inv_station_no_id = instat
            irr_entry.supl_fk_id = sup 
            irr_entry.save()
            return redirect('WISH.views.irr_entry_cont', ipk=irr_entry.pk, pk=pk, instat=instat)
    else:
        form = IRR_entryForm()
    return render(request, 'WISH/irr_entry.html', {'form': form})


def irr_entry_cont(request, ipk, pk, instat):
    if request.method == "POST":
        form = IRR_entry_cont_Form(request.POST)
        iform = IRR_entryForm()
        if form.is_valid():
            irr_entry_cont = form.save(commit=False)
            irr_entry_cont.asset_code_fk_id = pk 
            irr_entry_cont.irr_no_fk_id = ipk
            irr_entry_cont.quantity_rejected = irr_entry_cont.quantity_actual - irr_entry_cont.quantity_accepted
            irr_entry_cont.quantity_balance = irr_entry_cont.quantity_rejected
            irr_entry_cont.save()
            return redirect('WISH.views.miv_entry', pk=irr_entry_cont.pk, ipk=ipk, prk=pk, instat=instat, cpk=irr_entry_cont.cost_center_no_fk_id)
    else:
        form = IRR_entry_cont_Form()
    return render(request, 'WISH/irr_entry_cont.html', {'form': form})

def miv_entry(request, pk, ipk, prk, instat, cpk):
    if request.method == "POST":
        form = MIV_entryForm(request.POST)
        if form.is_valid():
            miv_entry = form.save(commit=False)
            miv_entry.doc_date = time.strftime("%Y-%m-%d")
            miv_entry.wrs_num = randint(100000,999999)
            miv_entry.asset_code_fk_id = prk
            miv_entry.amount = miv_entry.asset_code_fk.unit_cost * miv_entry.quantity 
            miv_entry.irr_no_fk_id = ipk
            miv_entry.inv_station_no_fk_id = instat
            miv_entry.cost_center_no_fk_id = cpk
            miv_entry.save()
            return redirect('WISH.views.irr_miv_form', mpk=miv_entry.pk, ipk=pk)
    else:
        form = MIV_entryForm()
    return render(request, 'WISH/miv_entry.html', {'form': form})

def par_entry(request):
    if request.method == "POST":
        form = PAR_entryForm(request.POST)
        if form.is_valid():
            par_entry = form.save(commit=False)
            par_entry.par_date = time.strftime("%Y-%m-%d")
            par_entry.save()
            return redirect('WISH.views.par_form')
    else:
        form = PAR_entryForm()
    return render(request, 'WISH/par_entry.html', {'form': form})

def wrs_form(request):
    wrss = MIV.objects.filter(pk=1)
    return render(request, 'WISH/wrs_form.html', {'wrss': wrss})

def par_form(request):
    pars = PAR.objects.all()
    return render(request, 'WISH/par_form.html', {'pars': pars})

def garv_form(request):
    garvs = GARV.objects.all()
    return render(request, 'WISH/garv_form.html', {'garvs': garvs})

def cme_form(request):
    return render(request, 'WISH/cme_form.html', {})

def irr_form(request):
    irs = IRR.objects.all()
    return render(request, 'WISH/irr_form.html', {'irs':irs})

def irr_miv_form(request, mpk, ipk):
    mivs = get_object_or_404(MIV, pk=mpk)
    irs = get_object_or_404(IRR, pk=ipk)
    amount = irs.quantity_accepted * irs.asset_code_fk.unit_cost
    total = amount
    return render(request, 'WISH/irr_miv_form.html', {'irs':irs , 'mivs':mivs, 'amount':amount, 'total':total})
    
def gatepass_form(request):
    return render(request, 'WISH/gatepass_form.html', {})

def miv_form(request):
    mivs = MIV.objects.all()
    return render(request, 'WISH/miv_form.html', {'mivs':mivs})
