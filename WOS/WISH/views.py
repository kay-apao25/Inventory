from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.db.models import Q
#from random import randint
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
        form1 = ProductForm1(request.POST)
        form2 = ProductForm2(request.POST)
        form3 = ProductForm3(request.POST)
        if form.is_valid() and form1.is_valid() and form2.is_valid() :
            product = form.save(commit=False)
            if len(Product.objects.all()) != 0:
                no = int((Product.objects.latest('id')).slc_number) + 1
                product.slc_number = str(no)
                for i in range(6-len(product.slc_number)):
                    product.slc_number = '0' + product.slc_number
            else:
                product.slc_number = '000000'

            for key in form.data.keys():
                key1 = key
                if key == 'inv_station_no' or key == 'purchased_from':
                    key = key + '_id'
                setattr(product, key, form1.data[key1])
                setattr(product, key, form2.data[key1])
                setattr(product, key, form3.data[key1])
                if form2.data['expiry_date'] == '':
                    product.expiry_date = None
                if int(form2.data['quantity']) > 1:
                    if form2.data['unit_measure'] == 'box':
                        product.unit_measure = str(product.unit_measure) + 'es'
                    else:
                        product.unit_measure = str(product.unit_measure) + 's'
            product.amount = int(form2.data['unit_cost']) * int(form2.data['quantity'])


            product.save()
            return redirect('WISH.views.index')
    else:
        form = ProductForm()
        form1 = ProductForm1()
        form2 = ProductForm2()
        form3 = ProductForm3()
    return render(request, 'WISH/product_add.html', {'form3': form3 , 'form1':form1, 'form2': form2})


def irr_entry(request):
    del prod_to_irr[:]
    del prod_to_par[:]
    del prod_to_garv[:]
    if request.method == "POST":
        form = IRR_entryForm(request.POST)
        form1 = IRR_entryForm1(request.POST)
        form2 = IRR_entryForm2(request.POST)
        if form.is_valid() and form1.is_valid():
            irr_entry = form.save(commit=False)
            if len(IRR.objects.all()) != 0:
                no = int((IRR.objects.latest('wrs_number')).irr_no) + 1
                irr_no = str(no)
                if (6-len(irr_no)) > 0:
                    for i in range(6-len(irr_no)):
                        irr_no = '0' + irr_no
            else:
                irr_no = '000000'

            for key in form.data.keys():
                key1 = key
                if key == 'supplier' or key == 'inv_station_no' or key == 'dce_user' or key == 'dce_approved':
                    key = key + '_id'
                setattr(irr_entry, key, form1.data[key1])
                setattr(irr_entry, key, form2.data[key1])

            irr_entry.dce_custodian = Employee.objects.get(name=(str(request.user.first_name) + ' ' + str(request.user.last_name)))

            irr_entry.save()
            return redirect('WISH.views.product_to_irr', pk=irr_entry.pk, irn=irr_no, inv=int(irr_entry.inv_station_no_id))
    else:
        form = IRR_entryForm()
        form1 = IRR_entryForm1()
        form2 = IRR_entryForm2()
    return render(request, 'WISH/irr_entry.html', {'form': form, 'form1': form1, 'form2': form2})

prod_to_irr = []
def product_to_irr(request, pk, irn, inv):
    if request.method == "POST":
        form = Product_to_IRRForm(request.POST)
        iform = IRR_entry_cont_Form(request.POST)
        if form.is_valid() and iform.is_valid():
            if Product.objects.get(id=int(form.data['product'])).status != 'Pending':
                prod_to_irr.append({'IRR_no': irn, 'Product': form.data['product'], 'quantity_accepted': \
                    int(form.data['quantity_accepted']), 'quantity_rejected':int(form.data['quantity_rejected']), \
                    'quantity_balance': int(form.data['quantity_balance'])})
            else:
                return render_to_response('WISH/product_to_irr.html',
                        { 'error': 'Product -' + str(Product.objects.get(id=int(form.data['product'])).item_name +  '- is still pending.'),
                        'form': form, 'iform': iform})
            irr = iform.save(commit=False)
            irr.irr_no = irn
            irr.irr_headkey_id = pk
            if len(IRR.objects.all()) != 0:
                no = int((IRR.objects.latest('wrs_number')).wrs_number) + 1
                irr.wrs_number = str(no)
            else:
                irr.wrs_number = irr.irr_headkey.inv_station_no.inv_station_no + '000000'
            res = json.dumps(prod_to_irr)
            irr.product = res
            prods = irr.product
            for prod in prods:
                p = Product.objects.get(id=(prod['Product']))
                p.quantity = int(prod['quantity_accepted'])
                p.balance = int(prod['quantity_balance'])
                if p.balance == 0:
                    p.status = 'Complete'
                    #p.remarks = 'Product has an IRR Record (IRR No: ' + irn + ')'
            p.save()
            irr.save()
            return redirect('WISH.views.product_to_irr', pk=pk, irn=irn, inv=int(inv))
    else:
        form = Product_to_IRRForm()
        iform = IRR_entry_cont_Form()
        form.fields['product'] = forms.ModelChoiceField(Product.objects.filter(inv_station_no=inv), label='Product *')
    return render(request, 'WISH/product_to_irr.html', {'form': form, 'iform': iform, 'pk': pk})

def miv_entry_S(request, pk):
    del prod_to_irr[:]
    del prod_to_par[:]
    del prod_to_garv[:]
    if request.method == "POST":
        form = MIV_entryForm(request.POST)
        if form.is_valid():
            miv_entry = form.save(commit=False)
            if len(MIV.objects.all()) != 0:
                no = int((MIV.objects.latest('id')).miv_no) + 1
                miv_entry.miv_no = str(no)
                if (6-len(miv_entry.miv_no)) < 0:
                    for i in range(6-len(miv_entry.miv_no)):
                        miv_entry.miv_no = '0' + miv_entry.miv_no
            else:
                miv_entry.miv_no = '000000'
            miv_entry.doc_date = time.strftime("%Y-%m-%d")
            miv_entry.irr_no_id = pk
            prods = miv_entry.irr_no.product
            for prod in prods:
                p = Product.objects.get(id=(prod['Product']))
                p.quantity = int(p.quantity) - int(prod['quantity_accepted'])
                if p.quantity < 0:
                    p.quantity = 0
                    return render_to_response('WISH/miv_entry.html',
                        { 'error': 'No stock for such item.',
                        'form': form })
                p.amount = int(p.unit_cost) * int(p.quantity)
                p.average_amount = p.amount
                #p.remarks = p.remarks + ', Product has a MIV Record (MIV No: ' + miv_entry.miv_no + ')'
            p.save()
            miv_entry.save()
            return redirect('WISH.views.index')
    else:
        form = MIV_entryForm()
    return render(request, 'WISH/miv_entry.html', {'form': form})

def miv_entry(request):
    del prod_to_irr[:]
    del prod_to_par[:]
    del prod_to_garv[:]
    irrs = IRR.objects.all()
    return render(request, 'WISH/miv_entry_f.html', {'irrs':irrs})

def par_f(request):
    del prod_to_irr[:]
    del prod_to_par[:]
    del prod_to_garv[:]
    irrs = IRR.objects.filter(is_par=False)
    return render(request, 'WISH/par_f.html', {'irrs':irrs})

def garv_entry_f(request):
    del prod_to_irr[:]
    del prod_to_par[:]
    del prod_to_garv[:]
    pars = PAR.objects.all()
    garvs = GARV.objects.all()
    return render(request, 'WISH/garv_entry_f.html', {'pars':pars, 'garvs':garvs})

prod_to_garv = []
def product_to_garv(request, pk):
    if request.method == "POST":
        form = GARV_entryForm(request.POST)
        iform = Product_to_GARVform(request.POST)
        if form.is_valid():
            prod_to_garv.append({'Product': iform.data['product'], 'Quantity': \
            iform.data['quantity'], 'PAR_number': pk, 'Remarks': \
            iform.data['remarks']})
            garv = form.save(commit=False)
            garv.garv_date = time.strftime("%Y-%m-%d")
            garv.dce = (PAR.objects.get(par_no=pk)).dce
            garv.garv_no = iform.data['garv_no']
            garv.wo_number = (PAR.objects.get(par_no=pk)).wo_number
            res = json.dumps(prod_to_garv)
            garv.product_to_GARV = res
            prods = garv.product_to_GARV
            for prod in prods:
                p = Product.objects.get(id=(prod['Product']))
                p.quantity = int(p.quantity) + int(prod['Quantity'])
                #p.remarks = 'Product has a GARV Record (GARV No: ' + garv.garv_no + ')'
            p.save()
            garv.save()
            return redirect('WISH.views.garv_entry', g=garv.garv_no, pk=pk)
    else:
        form = GARV_entryForm()
        iform = Product_to_GARVform()
        products = PAR.objects.get(par_no=pk).product
        iform.fields['product'] = forms.ModelChoiceField(Product.objects.all().filter(id__in=\
            [Product.objects.get(id=p['Product']).id for p in products]), label='Product *')
        form.fields['cc_number'] = forms.ModelChoiceField(Cost_center.objects.filter(id=PAR.objects.get(par_no=pk).inv_stat_no.cost_center_no.id), label='CC number*')
    return render(request, 'WISH/garv_entry.html', {'form': form, 'iform': iform})

def garv_entry(request, g, pk):
    if request.method == "POST":
        form = GARV_entryForm(request.POST)
        iform = Product_to_GARVform1(request.POST)
        if form.is_valid():
            prod_to_garv.append({'Product': iform.data['product'], 'Quantity': \
            iform.data['quantity'], 'PAR_number':pk, 'Remarks': iform.data['remarks']})
            garv = form.save(commit=False)
            garv.garv_date = time.strftime("%Y-%m-%d")
            garv.dce = (PAR.objects.get(par_no=pk)).dce
            garv.wo_number = (PAR.objects.get(par_no=pk)).wo_number
            garv.garv_no = g
            res = json.dumps(prod_to_garv)
            garv.product_to_GARV = res
            prods = garv.product_to_GARV
            for prod in prods:
                p = Product.objects.get(id=(prod['Product']))
                p.quantity = int(p.quantity) + int(prod['Quantity'])
                #p.remarks = 'Product has a GARV Record (GARV No: ' + garv.garv_no + ')'
            p.save()
            garv.save()
            return redirect('WISH.views.garv_entry', g=g, pk=pk)
    else:
        form = GARV_entryForm()
        iform = Product_to_GARVform1()
        products = PAR.objects.get(par_no=pk).product
        iform.fields['product'] = forms.ModelChoiceField(Product.objects.all().filter(id__in=\
            [Product.objects.get(id=p['Product']).id for p in products]), label='Product*')
        form.fields['cc_number'] = forms.ModelChoiceField(Cost_center.objects.filter(id=PAR.objects.get(par_no=pk).inv_stat_no.cost_center_no.id), label='CC number*')
    return render(request, 'WISH/garv_entry.html', {'form': form, 'iform': iform})

prod_to_par = []
prod_to_garv = []
def par(request, inv):
    if request.method == "POST":
        form = PAR_Form(request.POST)
        iform = Product_to_PARForm(request.POST)
        if form.is_valid() and iform.is_valid():
            par_entry = form.save(commit=False)
            par_entry.par_date = time.strftime("%Y-%m-%d")
            prod_to_par.append({'Product': iform.data['product'],\
                                'Quantity': iform.data['quantity']})
            amt_cost = 0
            for product in prod_to_par:
                pro = Product.objects.get(id=product['Product'])
                amount = float(product['Quantity']) * int(pro.unit_cost)
                amt_cost = amt_cost + amount
            par_entry.amt_cost = amt_cost
            res = json.dumps(prod_to_par)
            par_entry.product = prod_to_par
            par_entry.inv_stat_no_id = IRR.objects.get(irr_no=inv).irr_headkey.inv_station_no.id
            par_entry.par_no = iform.data['par_no']
            par_entry.issued_by = Employee.objects.get(name=(str(request.user.first_name) + ' ' + str(request.user.last_name)))
            #par_entry.PO_number_id = str(IRR.objects.get(irr_no=inv).irr_headkey.po_number)
            irr = IRR.objects.get(irr_no=inv)
            irr.is_par = 'True'
            irr.save()
            par_entry.save()
            return redirect('WISH.views.par_entry', pk=par_entry.par_no, inv=inv)
    else:
        form = PAR_Form()
        iform = Product_to_PARForm()
        form.fields['dce'] = forms.ModelChoiceField(Employee.objects.filter(\
            cost_center_no=IRR.objects.get(irr_no=inv).irr_headkey.inv_station_no.cost_center_no.id), label='Accountable Employee*')
        form.fields['approved_by'] = forms.ModelChoiceField(Employee.objects.filter(\
            cost_center_no=IRR.objects.get(irr_no=inv).irr_headkey.inv_station_no.cost_center_no.id), label='Approved by*')
        form.fields['issued_by'] = forms.ModelChoiceField(Employee.objects.filter(\
            cost_center_no=IRR.objects.get(irr_no=inv).irr_headkey.inv_station_no.cost_center_no.id), label='Issued by*')
        products = IRR.objects.get(irr_no=inv).product
        iform.fields['product'] = forms.ModelChoiceField(Product.objects.all().filter(id__in=\
            [Product.objects.get(id=p['Product']).id for p in products]), label='Product *')
    return render(request, 'WISH/par_entry.html', {'form': form, 'iform': iform})

def par_entry(request, pk, inv):
    if request.method == "POST":
        form = PAR_Form(request.POST)
        iform = Product_to_PARForm1(request.POST)
        if form.is_valid() and iform.is_valid():
            par_entry = form.save(commit=False)
            par_entry.par_date = time.strftime("%Y-%m-%d")
            prod_to_par.append({'Product': iform.data['product'],\
                                'Quantity': iform.data['quantity']})
            amt_cost = 0
            for product in prod_to_par:
                pro = Product.objects.get(id=product['Product'])
                amount = float(product['Quantity']) * int(pro.unit_cost)
                amt_cost = amt_cost + amount
            res = json.dumps(prod_to_par)
            par_entry.product = res
            par_entry.inv_stat_no_id = IRR.objects.get(irr_no=inv).irr_headkey.inv_station_no.id
            par_entry.amt_cost = amt_cost
            par_entry.par_date = time.strftime("%Y-%m-%d")
            par_entry.par_no = pk
            #par_entry.PO_number = str(IRR.objects.get(irr_no=inv).irr_headkey.po_number)
            irr = IRR.objects.get(irr_no=inv)
            irr.is_par = 'True'
            irr.save()
            par_entry.save()
            return redirect('WISH.views.par_entry', pk=pk, inv=inv)
    else:
        form = PAR_Form()
        iform = Product_to_PARForm1()
        form.fields['dce'] = forms.ModelChoiceField(Employee.objects.filter(\
            cost_center_no=IRR.objects.get(irr_no=inv).irr_headkey.inv_station_no.cost_center_no.id))
        form.fields['approved_by'] = forms.ModelChoiceField(Employee.objects.filter(\
            cost_center_no=IRR.objects.get(irr_no=inv).irr_headkey.inv_station_no.cost_center_no.id))
        form.fields['issued_by'] = forms.ModelChoiceField(Employee.objects.filter(\
            cost_center_no=IRR.objects.get(irr_no=inv).irr_headkey.inv_station_no.cost_center_no.id))
        products = IRR.objects.get(irr_no=inv).product
        iform.fields['product'] = forms.ModelChoiceField(Product.objects.all().filter(id__in=\
            [Product.objects.get(id=p['Product']).id for p in products]))
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

def product_details(request, pk):
    prod = get_object_or_404(Product, pk=pk)
    return render(request, 'WISH/product_details.html', {'prod': prod})

def product_form(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        form1 = ProductForm5.ProductForm1(request.POST)
        form2 = ProductForm5.ProductForm2(request.POST)
        form3 = ProductForm5.ProductForm3(request.POST)
        if form.is_valid(): #form1.is_valid() and form2.is_valid() and form3.is_valid():
            prod = form.save(commit=False)
            prod.slc_number = product.slc_number
            if form2.data['expiry_date'] == '':
                prod.expiry_date = None
            if int(form2.data['quantity']) > 1:
                if form2.data['unit_measure'] == 'box':
                    prod.unit_measure = str(product.unit_measure) + 'es'
                else:
                    prod.unit_measure = str(product.unit_measure) + 's'
            prod.amount = int(form2.data['unit_cost']) * int(form2.data['quantity'])

            for key in form.data.keys():
                key1 = key
                if key == 'inv_station_no' or key == 'purchased_from':
                    key = key + '_id'
                setattr(prod, key, form1.data[key1])
                setattr(prod, key, form2.data[key1])
                setattr(prod, key, form3.data[key1])
            prod.save()
            #product.save()
            return redirect('WISH.views.index')
    else:
        form = ProductForm5(instance=product)
        form1 = ProductForm5.ProductForm1()
        form2 = ProductForm5.ProductForm2()
        form3 = ProductForm5.ProductForm3()
        for key in form.fields.keys():
            for key1 in form1.fields.keys():
                if key == key1:
                    form1.fields[key].initial = getattr(product, key)
            for key2 in form2.fields.keys():
                if key == key2:
                    form2.fields[key].initial = getattr(product, key)
            for key3 in form3.fields.keys():
                if key == key3:
                    form3.fields[key].initial = getattr(product, key)
    return render(request, 'WISH/product_form.html', {'form1': form1, 'form2': form2, 'form3': form3 })


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
    products = garvs.product_to_GARV
    total = 0
    for product in products:
        pro = Product.objects.get(id=product['Product'])
        #amount = float(product['quantity_accepted']) * int(pro.unit_cost)
        #product['amount'] = amount
        product['pros'] = pro
        #total = total + amount
    return render(request, 'WISH/garv_form.html', {'garvs': garvs, 'products': products})

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
    mivs = get_object_or_404(MIV, miv_no=pk)
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
