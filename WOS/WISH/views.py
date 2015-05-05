from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from random import randint
from .models import *
from .forms import *
import time
import json

# Create your views here.
def index(request):
    del prod_to_irr[:]
    del prod_to_par[:]
    del prod_to_garv[:]
    return render(request, 'WISH/index.html', {})

def wrs_num(request):
    return render(request, 'WISH/wrs_num.html', {})

def file_report(request):
    del prod_to_irr[:]
    del prod_to_par[:]
    del prod_to_garv[:]
    return render(request, 'WISH/file_report.html', {})

def irr_reports(request):
    irrs = IRR.objects.all()
    return render(request, 'WISH/irr_reports.html', {'irrs': irrs})

def miv_reports(request):
    mivs = MIV.objects.all()
    return render(request, 'WISH/miv_reports.html', {'mivs': mivs})

def wrs_reports(request):
    wrss = IRR.objects.all()
    return render(request, 'WISH/wrs_reports.html', {'wrss': wrss})

def par_reports(request):
    pars = PAR.objects.all()
    return render(request, 'WISH/par_reports.html', {'pars': pars})

def garv_reports(request):
    garvs = GARV.objects.all()
    return render(request, 'WISH/garv_reports.html', {'garvs': garvs})

def product_reports(request):
    prods = Product.objects.all()
    return render(request, 'WISH/product_reports.html', {'prods': prods})

def file_entry(request):
    return render(request, 'WISH/file_entry.html', {})

def product_new(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.slc_number = randint(100000,999999)
            product.nsn = randint(500000,999999)
            #product.cost_center_no_id = product.inv_station_no.cost_center_no_id
            product.amount = product.unit_cost * product.quantity
            product.save()
            return redirect('WISH.views.index')
            #return redirect('WISH.views.irr_entry', pk=product.pk, instat=product.inv_station_no_fk_id, sup=product.purchased_from_id)
    else:
        form = ProductForm()
    return render(request, 'WISH/product_add.html', {'form': form})


def irr_entry(request):
    del prod_to_irr[:]
    del prod_to_par[:]
    del prod_to_garv[:]
    if request.method == "POST":
        form = IRR_entryForm(request.POST)
        if form.is_valid():
            irr_entry = form.save(commit=False)
            irr_no = randint(100000,999999)
            irr_entry.save()
            return redirect('WISH.views.product_to_irr', pk=irr_entry.pk, irn=irr_no)#, inv=irr_entry.inv_station_no)
            #return redirect('WISH.views.irr_entry_cont', pk=irr_entry.pk)
    else:
        form = IRR_entryForm()
    return render(request, 'WISH/irr_entry.html', {'form': form})

"""def try_entry(request):
    if request.method == "POST":
        form = TryForm(request.POST)
        if form.is_valid():
            irr_entry = form.save(commit=False)
            #irr_no = randint(100000,999999)
            irr_entry.save()
            #return redirect('WISH.views.product_to_irr', pk=irr_entry.pk, irn=irr_no)
            return redirect('WISH.views.index')
    else:
        form = TryForm()
    return render(request, 'WISH/irr_entry.html', {'form': form})"""

prod_to_irr = []
def product_to_irr(request, pk, irn):
    if request.method == "POST":
        form = Product_to_IRRForm(request.POST)
        iform = IRR_entry_cont_Form(request.POST)
        if form.is_valid() and iform.is_valid():
            prod_to_irr.append({'IRR_no': irn, 'Product': form.data['product'], 'quantity_accepted': \
                int(form.data['quantity_accepted']), 'quantity_rejected':int(form.data['quantity_rejected']), \
                'quantity_balance': int(form.data['quantity_balance'])})
            irr = iform.save(commit=False)
            irr.irr_no = irn
            irr.irr_headkey_id = pk
            irr.wrs_number = randint(100000,999999)
            res = json.dumps(prod_to_irr)
            irr.product = res
            irr.save()
            return redirect('WISH.views.product_to_irr', pk=pk, irn=irn)
    else:
        form = Product_to_IRRForm()
        iform = IRR_entry_cont_Form()
        #form.fields['product'] = forms.ModelChoiceField(Product_to_PAR.objects.filter(par_no=pk))
    return render(request, 'WISH/product_to_irr.html', {'form': form, 'iform': iform, 'pk': pk})

"""def irr_entry_cont(request, pk):
    if request.method == "POST":
        form = IRR_entry_cont_Form(request.POST)
        #iform = IRR_entryForm()

        if form.is_valid():
            irr_entry_cont = form.save(commit=False)
            irr_entry_cont.irr_no = randint(100000,999999)
            irr_entry_cont.irr_headkey_id = pk
            irr_entry.wrs_number = randint(100000,999999)
            #irr_entry_cont.quantity_rejected = irr_entry_cont.quantity_actual - irr_entry_cont.quantity_accepted
            #irr_entry_cont.quantity_balance = irr_entry_cont.quantity_rejected
            #for product in irr.asset_code():

            irr_entry_cont.save()
            return redirect('WISH.views.product_to_irr', pk=irr_entry_cont.pk)
    else:
        form = IRR_entry_cont_Form()
    return render(request, 'WISH/irr_entry_cont.html', {'form': form})"""

def miv_entry_S(request, pk):
    del prod_to_irr[:]
    del prod_to_par[:]
    del prod_to_garv[:]
    if request.method == "POST":
        form = MIV_entryForm(request.POST)
        if form.is_valid():
            miv_entry = form.save(commit=False)
            miv_entry.doc_date = time.strftime("%Y-%m-%d")
            miv_entry.irr_no_id = pk
            #miv_entry.irr_headkey = miv_entry.product.irr_headkey
            miv_entry.cost_center_no_id = miv_entry.inv_station_no.cost_center_no_id
            #miv_entry.amount = miv_entry.asset_code.unit_cost * miv_entry.quantity
            miv_entry.save()
            return redirect('WISH.views.index')
    else:
        form = MIV_entryForm()
    return render(request, 'WISH/miv_entry.html', {'form': form })

def miv_entry(request):
    if request.method == "POST":
        form = MIV_entryForm(request.POST)
        if form.is_valid():
            miv_entry = form.save(commit=False)
            miv_entry.save()
            return redirect('WISH.views.index')
    else:
        irrs = IRR.objects.all()
    #    pros = Product_to_IRR.objects.all()
    return render(request, 'WISH/miv_entry_f.html', {'irrs':irrs})

def garv_entry_f(request):
    del prod_to_irr[:]
    del prod_to_par[:]
    del prod_to_garv[:]
    if request.method == "POST":
        form = GARV_entryForm(request.POST)
        if form.is_valid():
            garv_entry = form.save(commit=False)
            garv_entry.save()
            return redirect('WISH.views.index')
    else:
        pars = PAR.objects.all()
        garvs = GARV.objects.all()
    return render(request, 'WISH/garv_entry_f.html', {'pars':pars, 'garvs':garvs})

def garv_entry(request, pk):
    if request.method == "POST":
        form = GARV_entryForm(request.POST)
        if form.is_valid():
            garv_entry = form.save(commit=False)
            garv_entry.garv_date = time.strftime("%Y-%m-%d")
            garv_entry.save()
            return redirect ('WISH.views.index')
            #return redirect('WISH.views.garv_form', pk = garv_entry.pk)
    else:
        form = GARV_entryForm()
        form.fields['product'] = forms.ModelChoiceField(Product_to_PAR.objects.filter(par_no=pk))
    return render(request, 'WISH/garv_entry.html', {'form': form})

prod_to_garv = []
def product_to_garv(request,pk):
    if request.method == "POST":
        form = GARV_entryForm(request.POST)
        iform = Product_to_GARVform(request.POST)
        if form.is_valid():
            prod_to_garv.append({'Product': iform.data['product'], 'Quantity': \
            iform.data['qty'], 'PAR number':iform.data['par_number'], 'Remarks': \
            iform.data['remarks']})
            garv = form.save(commit=False)
            garv.garv_date = time.strftime("%Y-%m-%d")
            res = json.dumps(prod_to_garv)
            garv.product_to_GARV = res
            garv.save()
            return redirect('WISH.views.product_to_garv', pk=pk)
    else:
        form = GARV_entryForm()
        par = PAR.objects.get(dce=pk)
        iform = Product_to_GARVform()#products= par.product)
        #iform.fields['product'] = forms.ModelChoiceField(PAR.objects.filter(par_no=par))
    return render(request, 'WISH/garv_entry.html', {'form': form, 'iform': iform, 'pk': pk})

prod_to_par = []
prod_to_garv = []


def par(request):
    if request.method == "POST":
        form = PAR_entryForm(request.POST)
        iform = Product_to_PARForm(request.POST)
        if form.is_valid() and iform.is_valid():
            par_entry = form.save(commit=False)
            par_entry.par_date = time.strftime("%Y-%m-%d")
            prod_to_par.append({'Product': 'hgfgd',\
                                'Quantity': 'jhghgfhf'})
            res = json.dumps(prod_to_par)
            par_entry.product = prod_to_par
            par_entry.save()
            return redirect('WISH.views.par_entry', pk=par_entry.par_no)
    else:
        form = PAR_entryForm()
        iform = Product_to_PARForm()
    return render(request, 'WISH/par_entry.html', {'form': form, 'iform': iform})

def par_entry(request, pk):
    if request.method == "POST":
        form = PAR_Form(request.POST)
        iform = Product_to_PARForm(request.POST)
        if form.is_valid() and iform.is_valid():
            par_entry = form.save(commit=False)
            par_entry.par_date = time.strftime("%Y-%m-%d")
            prod_to_par.append({'Product': iform.data['product'],\
                                'Quantity': iform.data['qty']})
            res = json.dumps(prod_to_par)
            par_entry.product = res
            par_entry.par_date = time.strftime("%Y-%m-%d")
            par_entry.par_no = pk
            par_entry.save()
            return redirect('WISH.views.par_entry', pk=pk)
    else:
        form = PAR_Form()
        iform = Product_to_PARForm()
    return render(request, 'WISH/par_entry.html', {'form': form, 'iform': iform})

def wrs_entry(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        return redirect('WISH.views.wrs_form', pk=q)
    return render(request, 'WISH/wrs_entry.html', {})

def wrs_form(request, pk):
    wrss = get_object_or_404(IRR, wrs_number=pk)
    pros = wrss.product
    for pro in pros:
        pro['product'] = Product.objects.get(id=pro['Product'])
    return render(request, 'WISH/wrs_form.html', {'wrss': wrss, 'pros': pros})

def par_form(request, pk):
    parss = get_object_or_404(PAR, pk=pk)
    products = parss.product
    total = 0
    for product in products:
        pro = Product.objects.get(id=product['Product'])
        amount = float(product['Quantity']) * int(pro.unit_cost)
        product['amount'] = amount
        product['pros'] = pro
        product['description'] = pro.description
        product['item_name'] = pro.item_name
        product['unit'] = pro.unit_measure
        product['from'] = pro.purchased_from
        total = total + amount
    return render(request, 'WISH/par_form.html', {'parss':parss, 'products': products, 'total': total})

def garv_form(request, pk):
    garvs = get_object_or_404(GARV, pk=pk)
    pros = Product_to_GARV.objects.filter(garv=pk)
    return render(request, 'WISH/garv_form.html', {'garvs': garvs, 'pros': pros})

def cme_form(request):
    return render(request, 'WISH/cme_form.html', {})

def irr_form(request, pk):
    irs = get_object_or_404(IRR, pk=pk)
    products = irs.product
    total = 0
    for product in products:
        pro = Product.objects.get(id=product['Product'])
        amount = float(product['quantity_accepted']) * int(pro.unit_cost)
        product['amount'] = amount
        product['pros'] = pro
        total = total + amount
    return render(request, 'WISH/irr_form.html', {'irs':irs, 'products': products, \
                     'total': total})

def gatepass_form(request):
    return render(request, 'WISH/gatepass_form.html', {})

def miv_form(request, pk):
    mivs = get_object_or_404(MIV, pk=pk)
    products = mivs.irr_no.product
    amt_list = {}
    total = 0
    for product in products:
        pro = Product.objects.get(id=product['Product'])
        amount = float(product['quantity_accepted']) * int(pro.unit_cost)
        product['amount'] = amount
        product['pros'] = pro
        total = total + amount
    return render(request, 'WISH/miv_form.html', {'mivs':mivs, 'products':products, \
                    'amt_list': amt_list, 'total': total})

def irr_report(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        return redirect('WISH.views.irr_form', pk=q)
    return render(request, 'WISH/irr_report.html', {})

def miv_report(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        return redirect('WISH.views.miv_form', pk=q)
    return render(request, 'WISH/miv_report.html', {})

def par_report(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        return redirect('WISH.views.par_form', pk=q)
    return render(request, 'WISH/par_report.html', {})

def garv_report(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        return redirect('WISH.views.garv_form', pk=q)
    return render(request, 'WISH/garv_report.html', {})
