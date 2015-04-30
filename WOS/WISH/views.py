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

def file_report(request):
    return render(request, 'WISH/file_report.html', {})

def irr_reports(request):
    irrs = IRR.objects.all()
    return render(request, 'WISH/irr_reports.html', {'irrs': irrs})

def miv_reports(request):
    mivs = MIV.objects.all()
    return render(request, 'WISH/miv_reports.html', {'mivs': mivs})

def wrs_reports(request):
    wrss = MIV.objects.all()
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
    if request.method == "POST":
        form = IRR_entryForm(request.POST)
        if form.is_valid():
            irr_entry = form.save(commit=False)
            irr_no = randint(100000,999999)
            irr_entry.save()
            return redirect('WISH.views.product_to_irr', pk=irr_entry.pk, irn=irr_no)
            #return redirect('WISH.views.irr_entry_cont', pk=irr_entry.pk)
    else:
        form = IRR_entryForm()
    return render(request, 'WISH/irr_entry.html', {'form': form})

def product_to_irr(request,pk, irn):
    if request.method == "POST":
        form = Product_to_IRRForm(request.POST)
        iform = IRR_entry_cont_Form(request.POST)
        if form.is_valid() and iform.is_valid():
            product_to_irr = form.save(commit=False)
            irr = iform.save(commit=False)
            irr.irr_no = irn
            irr.irr_headkey_id = pk
            product_to_irr.irr_no_id= irn
            #product_to_irr.product = product_to_irr.
            #iform.fields['cost_center_no'].initial = iform.cleaned_data['cost_center_no']
            irr.save()
            product_to_irr.save()
            #form = Product_to_IRRForm(request.POST) 
            return redirect('WISH.views.product_to_irr', pk=pk, irn=irn)
    else:
        form = Product_to_IRRForm()
        iform = IRR_entry_cont_Form()
    return render(request, 'WISH/product_to_irr.html', {'form': form, 'iform': iform, 'pk': pk})

def irr_entry_cont(request, pk):
    if request.method == "POST":
        form = IRR_entry_cont_Form(request.POST)
        #iform = IRR_entryForm()

        if form.is_valid():
            irr_entry_cont = form.save(commit=False)
            irr_entry_cont.irr_no = randint(100000,999999)
            irr_entry_cont.irr_headkey_id = pk
            #irr_entry_cont.quantity_rejected = irr_entry_cont.quantity_actual - irr_entry_cont.quantity_accepted
            #irr_entry_cont.quantity_balance = irr_entry_cont.quantity_rejected
            #for product in irr.asset_code():

            irr_entry_cont.save()
            return redirect('WISH.views.product_to_irr', pk=irr_entry_cont.pk)
    else:
        form = IRR_entry_cont_Form()
    return render(request, 'WISH/irr_entry_cont.html', {'form': form})

def miv_entry_S(request, pk):
    if request.method == "POST":
        form = MIV_entryForm(request.POST)
        if form.is_valid():
            miv_entry = form.save(commit=False)
            miv_entry.doc_date = time.strftime("%Y-%m-%d")
            miv_entry.wrs_number = randint(100000,999999)
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
        pros = Product_to_IRR.objects.all()
    return render(request, 'WISH/miv_entry_f.html', {'irrs':irrs, 'pros':pros})

def garv_entry_f(request):
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

def product_to_garv(request,pk):
    if request.method == "POST":
        form = GARV_entryForm(request.POST)
        iform = Product_to_GARVform(request.POST)
        if form.is_valid() and iform.is_valid():
            product_to_garv = iform.save(commit=False)
            garv = form.save(commit=False)
            garv.garv_date = time.strftime("%Y-%m-%d")
            form = Product_to_GARVform(request.POST)
            garv.save()
            product_to_garv.garv_id = garv.pk
            product_to_garv.save()
            return redirect('WISH.views.product_to_garv', pk=garv.garv_no)
    else:
        form = GARV_entryForm()
        iform = Product_to_GARVform()
        par = PAR.objects.filter(dce=pk)
        iform.fields['product'] = forms.ModelChoiceField(Product_to_PAR.objects.filter(par_no=par))
        #iform.fields['par_number'] = forms.ModelChoiceField(Product_to_PAR.objects.filter(par_no=par))
    return render(request, 'WISH/garv_entry.html', {'form': form, 'iform': iform, 'pk': pk})

def par(request):
    if request.method == "POST":
        form = PAR_entryForm(request.POST)
        iform = Product_to_PARForm(request.POST)
        if form.is_valid() and iform.is_valid():
            par_entry = form.save(commit=False)
            par_pro = form.save(commit=False)
            par_entry.par_date = time.strftime("%Y-%m-%d")
            par_entry.save()
            par_pro.save()
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
            par_pro = form.save(commit=False)
            par_entry.par_date = time.strftime("%Y-%m-%d")
            par_entry.par_no = pk
            par_entry.save()
            par_pro.save()
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
    wrss = get_object_or_404(MIV, wrs_number=pk)
    pros = Product_to_IRR.objects.filter(irr_no=wrss.irr_no)
    return render(request, 'WISH/wrs_form.html', {'wrss': wrss, 'pros': pros})

def par_form(request, pk):
    pars = get_object_or_404(PAR, pk=pk)
    return render(request, 'WISH/par_form.html', {'pars': pars})

def garv_form(request, pk):
    garvs = get_object_or_404(GARV, pk=pk)
    return render(request, 'WISH/garv_form.html', {'garvs': garvs})

def cme_form(request):
    return render(request, 'WISH/cme_form.html', {})

def irr_form(request, pk):
    irs = get_object_or_404(IRR, pk=pk)
    pros = Product_to_IRR.objects.filter(irr_no=pk)
    amt_list = {}
    total = 0
    for pro in pros:
        amount = pro.quantity_accepted * pro.product.unit_cost
        pro.amt = amount
        total = total + amount
    return render(request, 'WISH/irr_form.html', {'irs':irs, 'pros': pros, \
                    'amt_list': amt_list, 'total': total})

#def irr_miv_form(request, mpk, ipk):
#    mivs = get_object_or_404(MIV, pk=mpk)
#    irs = get_object_or_404(IRR, pk=ipk)
#    amount = irs.quantity_accepted * irs.asset_code.unit_cost
#    total = amount
#    return render(request, 'WISH/irr_miv_form.html', {'irs':irs , 'mivs':mivs, 'amount':amount, 'total':total})

def gatepass_form(request):
    return render(request, 'WISH/gatepass_form.html', {})

def miv_form(request, pk):
    mivs = get_object_or_404(MIV, pk=pk)
    pros = Product_to_IRR.objects.filter(irr_no=mivs.irr_no)
    amt_list = {}
    total = 0
    for pro in pros:
        amount = pro.quantity_accepted * pro.product.unit_cost
        pro.amt = amount
        total = total + amount
    return render(request, 'WISH/miv_form.html', {'mivs':mivs, 'pros': pros, \
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
