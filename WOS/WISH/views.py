from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
#from django.template import RequestContext
from django.contrib import messages
from django.db.models import Q
#from random import randint
from .models import *
from .forms import *
import time
import json

# Create your views here.
#msg = ''
def index(request):
    del prod_to_irr[:]
    del prod_to_par[:]
    del prod_to_garv[:]
    return render(request, 'WISH/index.html', {})

def aboutus(request):
    return render(request, 'WISH/AboutUs.html', {})

def wrs_num(request):
    return render(request, 'WISH/wrs_num.html', {})

def inv_stat_del(request, pk):
    inv_del = get_object_or_404(Inventory_stat, pk=pk)
    inv_del.is_delete = True
    inv_del.save()
    return render(request, 'WISH/index.html', {})

def cost_center_del(request, pk):
    cos_del = get_object_or_404(Cost_center, pk=pk)
    cos_del.is_delete = True
    cos_del.save()
    return render(request, 'WISH/index.html', {})

def file_report(request):
    del prod_to_irr[:]
    del prod_to_par[:]
    del prod_to_garv[:]
    return render(request, 'WISH/file_report.html', {})

def libraries(request):
    del prod_to_irr[:]
    del prod_to_par[:]
    del prod_to_garv[:]
    return render(request, 'WISH/libraries.html', {})

def inv_stat(request):
    inv = Inventory_stat.objects.filter(is_delete=False)
    return render(request, 'WISH/inv_stat.html', {'inv': inv})

def cost_center(request):
    cos = Cost_center.objects.filter(is_delete=False)
    return render(request, 'WISH/cost_center.html', {'cos': cos})

def supplier(request):
    sup = Supplier.objects.all()
    return render(request, 'WISH/supplier.html', {'sup': sup})

def employee(request):
    em = Employee.objects.all()
    return render(request, 'WISH/employee.html', {'em': em})


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

def stat_lib(request):
    if request.method == "POST":
        form = Stat_lib(request.POST)
        if form.is_valid() :
            product = form.save(commit=False)


            product.save()
            return redirect('WISH.views.index')

    else:
        form = Stat_lib()
    return render(request, 'WISH/stat_lib.html', {'form': form })

def product_new(request):
    if request.method == "POST":

        #Forms containing the entries entered by the user
        form = ProductForm(request.POST)
        form1 = ProductForm1(request.POST)
        form2 = ProductForm2(request.POST)
        form3 = ProductForm3(request.POST)

        #Non-empty forms are to be validated.
        if form.is_valid() and form1.is_valid() and form2.is_valid() :

            product = form.save(commit=False)

            #Generation of SLC number
            if len(Product.objects.all()) != 0:
                no = int((Product.objects.latest('id')).slc_number) + 1
                product.slc_number = str(no)
                for i in range(6-len(product.slc_number)):
                    product.slc_number = '0' + product.slc_number
            else:
                product.slc_number = '000000'

            #Assignment of values in Product model
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

            #Message to be returned if adding of the new product entry.
            msg = 'Product (' + form1.data['item_name'] + ') was added successfully.'

            #Displaying of blank forms
            form1 = ProductForm1()
            form2 = ProductForm2()
            form3 = ProductForm3()
    else:
        #Displaying of blank forms
        form = ProductForm()
        form1 = ProductForm1()
        form2 = ProductForm2()
        form3 = ProductForm3()

    #Rendering of forms and/or messages
    try:
        return render(request, 'WISH/product_add.html', {'form3': form3 , 'form1':form1, 'form2': form2, 'msg': msg})
    except:
        return render(request, 'WISH/product_add.html', {'form3': form3 , 'form1':form1, 'form2': form2})

def irr_entry(request):

    #Cleaning of Product_to_IRR, Product_to_PAR and Product_to_GARV lists
    del prod_to_irr[:]
    del prod_to_par[:]
    del prod_to_garv[:]

    if request.method == "POST":

        #Forms containing the entries entered by the user
        form = IRR_entryForm(request.POST)
        form1 = IRR_entryForm1(request.POST)
        form2 = IRR_entryForm2(request.POST)

        #Non-empty forms are to be validated.
        if form.is_valid() and form1.is_valid():
            irr_entry = form.save(commit=False)

            #Assignment of values in IRR header model
            for key in form.data.keys():
                key1 = key
                if key == 'supplier' or key == 'inv_station_no' or key == 'dce_user' or key == 'dce_approved':
                    key = key + '_id'
                setattr(irr_entry, key, form1.data[key1])
                setattr(irr_entry, key, form2.data[key1])

            irr_entry.dce_custodian = Employee.objects.get(name=(str(request.user.first_name) + ' ' + str(request.user.last_name)))
            irr_entry.save()

            return redirect('WISH.views.product_to_irr', pk=irr_entry.pk, inv=int(irr_entry.inv_station_no_id))
    else:
        pform = Product_to_IRRForm()
        pform.fields['product'].queryset = Product.objects.filter(is_irr=False)

        #To check if there are no available products to be made with IRR record
        if len(pform.fields['product'].queryset) == 0:
            #If true return this exit message
            exit = 'No available products to be made with IRR record.'
        else:
            #else display blank forms.
            form = IRR_entryForm()
            form1 = IRR_entryForm1()
            form2 = IRR_entryForm2()

    #Rendering of forms
    try:
        return render(request, 'WISH/irr_entry.html', {'exit': exit})
    except:
        return render(request, 'WISH/irr_entry.html', {'form': form, 'form1': form1, 'form2': form2})


prod_to_irr = [] #Product_to_IRR list: List for storing products to be added in a specific IRR form
def product_to_irr(request, pk, inv):
    if request.method == "POST":

        #Forms containing the entries entered by the user
        form = Product_to_IRRForm(request.POST)
        iform = IRR_entry_cont_Form(request.POST)

        #Non-empty forms are to be validated.
        if form.is_valid() and iform.is_valid():

            #To check if the desired quantity of products to be delivered are delivered already.
            if int(form.data['quantity_balance']) == 0:
                p = Product.objects.get(id=int(form.data['product']))
                p.balance = 0
                p.status = 'Complete'
                p.save()

            #To check if quantity accepted entered is less than the present stocked items.
            if Product.objects.get(id=int(form.data['product'])).quantity < int(form.data['quantity_accepted']):
                error = 'Accepted quantity is greater than the number of stocked items.'

            #To check if the delivering process of the product is already completed.
            elif Product.objects.get(id=int(form.data['product'])).status == 'Pending':
                error = 'Product -' + str(Product.objects.get(id=int(form.data['product'])).item_name) +  '- is still pending.'

            else:
                #Storing of products for this specific IRR form.
                prod_to_irr.append({'Product': form.data['product'], 'quantity_accepted': \
                    int(form.data['quantity_accepted']), 'quantity_rejected':int(form.data['quantity_rejected']), \
                    'quantity_balance': int(form.data['quantity_balance']), 'is_par':False, \
                    'quantity_par': int(form.data['quantity_accepted'])})
                p = Product.objects.get(id=int(form.data['product']))
                p.quantity = int(form.data['quantity_accepted'])
                p.balance = int(form.data['quantity_balance'])
                p.is_irr = True
                #p.remarks = 'Product has an IRR Record (IRR No: ' + irn + ')'
                p.save()

                irr = iform.save(commit=False)

                #Generation of IRR number
                if len(IRR.objects.all()) != 0:
                    no = int((IRR.objects.latest('wrs_number')).irr_no) + 1
                    irr.irr_no = str(no)
                    if (6-len(irr.irr_no)) > 0:
                        for i in range(6-len(irr.irr_no)):
                            irr.irr_no = '0' + irr.irr_no
                else:
                    irr.irr_no = '000000'

                irr.irr_headkey_id = pk

                #Generation of WRS number
                if len(IRR.objects.all()) != 0:
                    no = int((IRR.objects.latest('wrs_number')).wrs_number) + 1
                    irr.wrs_number = str(no)
                else:
                    irr.wrs_number = irr.irr_headkey.inv_station_no.inv_station_no + '000000'

                irr.irr_headkey_id = pk

                res = json.dumps(prod_to_irr)
                irr.product = res

                #To check if all entries for the IRR form is filled.
                if iform.has_changed():
                    msg = 'IRR record (IRR No. - ' + irr.irr_no + ') was successfully added.'
                    irr.save()
                else:
                    msg = 'Item (' + str(Product.objects.get(id=int(form.data['product'])).item_name) + ') was successfully added'

                form.fields['product'].queryset = Product.objects.filter(inv_station_no=inv).filter(is_irr=False)

                if len(form.fields['product'].queryset) == 0:
                    #If true return this exit message
                    exit = 'No available products to be made with IRR record.'
                else:
                    #else display blank forms.
                    form = Product_to_IRRForm()
                    iform = IRR_entry_cont_Form()

    else:
        form = Product_to_IRRForm()
        form.fields['product'].queryset = Product.objects.filter(inv_station_no=inv).filter(is_irr=False)
        if len(form.fields['product'].queryset) == 0:
            #If true return this exit message
            exit = 'No available products to be made with IRR record.'
        else:
            #else display blank forms.
            iform = IRR_entry_cont_Form()

    #Rendering of forms and/or messages and/or errors
    try:
        try:
            return render(request, 'WISH/irr_entry.html', {'exit': exit})
        except:
            return render(request, 'WISH/product_to_irr.html', {'form': form, 'iform': iform, 'error': error})
    except:
        try:
            return render(request, 'WISH/product_to_irr.html', {'form': form, 'iform': iform, 'msg': msg})
        except:
            return render(request, 'WISH/product_to_irr.html', {'form': form, 'iform': iform})


def miv_entry_S(request, pk):

    #Cleaning of Product_to_IRR, Product_to_PAR and Product_to_GARV lists
    del prod_to_irr[:]
    del prod_to_par[:]
    del prod_to_garv[:]

    if request.method == "POST":

        #Forms containing the entries entered by the user
        form = MIV_entryForm(request.POST)

        #Non-empty forms are to be validated.
        if form.is_valid():

            #error = ''

            miv_entry = form.save(commit=False)
            miv_entry.irr_no_id = pk

            #Generation of MIV number
            if len(MIV.objects.all()) != 0:
                no = int((MIV.objects.latest('id')).miv_no) + 1
                miv_entry.miv_no = str(no)
                if (6-len(miv_entry.miv_no)) > 0:
                    for i in range(6-len(miv_entry.miv_no)):
                        miv_entry.miv_no = '0' + miv_entry.miv_no
            else:
                miv_entry.miv_no = '000000'

            miv_entry.doc_date = time.strftime("%Y-%m-%d")
            miv_entry.irr_no_id = pk

            prods = miv_entry.irr_no.product

            #Deducting the number of quantities to be pulled out by the user
            for prod in prods:
                p = Product.objects.get(id=(prod['Product']))
                p.quantity = int(p.quantity) - int(prod['quantity_accepted'])
                p.amount = int(p.unit_cost) * int(p.quantity)
                p.average_amount = p.amount
                #p.remarks = p.remarks + ', Product has a MIV Record (MIV No: ' + miv_entry.miv_no + ')'
                p.save()

            miv_entry.save()

            #Success message
            msg = 'MIV record (MIV No. - ' + miv_entry.miv_no + ') was successfully added.'

            #Exit message
            exit = 'Exit'

            for prod in prods:
                p = Product.objects.get(id=(prod['Product']))
                p.quantity = int(p.quantity) - int(prod['quantity_accepted'])
                if p.quantity < 0:
                    irr = IRR.objects.get(irr_no=pk)
                    irr.is_miv = True
                    irr.save()

    else:
        form = MIV_entryForm()

    #Rendering of forms and/or messages
    try:
        return render(request, 'WISH/miv_entry.html', {'msg': msg, 'exit': exit})
    except:
        return render(request, 'WISH/miv_entry.html', {'form': form})

def miv_entry(request):
    del prod_to_irr[:]
    del prod_to_par[:]
    del prod_to_garv[:]
    irrs = IRR.objects.filter(is_miv=False)
    if len(irrs) == 0:
        return render(request, 'WISH/miv_entry_f.html', {'exit':'No IRR records to be made with MIV record.'})
    else:
        return render(request, 'WISH/miv_entry_f.html', {'irrs':irrs})

def par_f(request):
    del prod_to_irr[:]
    del prod_to_par[:]
    del prod_to_garv[:]
    irrs = IRR.objects.filter(is_par=False)
    if len(irrs) == 0:
        return render(request, 'WISH/par_f.html', {'exit': 'No IRR records to be made with PAR record.'})
    else:
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
    prod_list = []
    error = ''
    par_no = 0
    msg = 3
    if request.method == "POST":
        form = PAR_Form(request.POST)
        iform = Product_to_PARForm(request.POST)
        if form.is_valid() and iform.is_valid():
            par_entry = form.save(commit=False)
            par_entry.par_date = time.strftime("%Y-%m-%d")
            prod_to_par.append({'Product': iform.data['product'],\
                                'Quantity': iform.data['quantity']})
            par_entry.amt_cost = 0
            for product in prod_to_par:
                pro = Product.objects.get(id=product['Product'])
                amount = float(product['Quantity']) * int(pro.unit_cost)
                par_entry.amt_cost = par_entry.amt_cost + amount

            res = json.dumps(prod_to_par)
            par_entry.product = prod_to_par
            par_entry.inv_stat_no_id = IRR.objects.get(irr_no=inv).irr_headkey.inv_station_no.id
            par_entry.par_no = iform.data['par_no']
            par_entry.issued_by = Employee.objects.get(name=(str(request.user.first_name) + ' ' + str(request.user.last_name)))
            #par_entry.PO_number_id = str(IRR.objects.get(irr_no=inv).irr_headkey.po_number)
            irr = IRR.objects.get(irr_no=inv)
            for prod in irr.product:
                if prod['Product'] == str(iform.data['product']):
                    prod['quantity_par'] = int(prod['quantity_par']) - int(iform.data['quantity'])
                    if prod['quantity_par'] < 0:
                        error = 'Entered quantity is greater than stocked items.'
                    elif prod['quantity_par'] == 0:
                        prod['quantity_par'] = 0
                        prod['is_par'] = True
                        irr.save()
                    else:
                        prod['quantity_par'] = prod['quantity_par']
                        prod_list.append(int(prod['Product']))
                        irr.save()
                if prod['is_par'] == False:
                    prod_list.append(int(prod['Product']))

            if par_no == 0:
                par_no = par_entry.par_no
            else:
                par_entry.par_no = par_no

            par_entry.save()
            if len(prod_list) == 0:
                irr.is_par = True
                irr.save()
                exit = 'Exit'
                return render(request, 'WISH/par_entry.html', {'exit': exit, 'msg': 'PAR Record (PAR No. - ' + str(par_no) + ') is successfully added.'})

            if form.has_changed():
                msg = 0
                par_no = 0
                form = PAR_Form()
                iform = Product_to_PARForm()

            else:
                if error == '':
                    msg = 1
                else:
                    msg = 2
            #return redirect('WISH.views.par_entry', pk=par_entry.par_no, inv=inv, msg=msg)
    else:
        form = PAR_Form()
        if par_no == 0:
            iform = Product_to_PARForm()
        else:
            iform = Product_to_PARForm1()

    form.fields['dce'].queryset = Employee.objects.filter(\
        cost_center_no=IRR.objects.get(irr_no=inv).irr_headkey.inv_station_no.cost_center_no.id)
    form.fields['approved_by'].queryset = Employee.objects.filter(\
        cost_center_no=IRR.objects.get(irr_no=inv).irr_headkey.inv_station_no.cost_center_no.id)

    products = IRR.objects.get(irr_no=inv).product

    for prod in products:
        if prod['is_par'] == False:
            prod_list.append(int(prod['Product']))
    iform.fields['product'].queryset = Product.objects.all().filter(id__in=\
        [Product.objects.get(id=p).id for p in prod_list])

    if int(msg) == 0:
        return render(request, 'WISH/par_entry.html', {'form': form, 'iform': iform, 'msg': 'PAR Record (PAR No. - ' + str(par_entry.par_no) + ') is successfully added.'})
    elif int(msg) == 1:
        return render(request, 'WISH/par_entry.html', {'form': form, 'iform': iform, 'msg': 'Item is successfully added.'})
    elif int(msg) == 2:
        return render(request, 'WISH/par_entry.html', {'form': form, 'iform': iform, 'error': 'Entered product quantity to be assigned to this employee is greater than stocked items.'})
    else:
        return render(request, 'WISH/par_entry.html', {'form': form, 'iform': iform})


"""def par_entry(request, pk, inv, msg):
    prod_list = []
    error = ''
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
            par_entry.issued_by = Employee.objects.get(name=(str(request.user.first_name) + ' ' + str(request.user.last_name)))
            par_entry.par_no = pk
            #par_entry.PO_number = str(IRR.objects.get(irr_no=inv).irr_headkey.po_number)
            irr = IRR.objects.get(irr_no=inv)
            for prod in irr.product:
                if prod['Product'] == str(iform.data['product']):
                    prod['quantity_par'] = int(prod['quantity_par']) - int(iform.data['quantity'])
                    if prod['quantity_par'] < 0:
                        error = 'Entered quantity is greater than stocked items.'
                    elif prod['quantity_par'] == 0:
                        prod['quantity_par'] = 0
                        prod['is_par'] = True
                        irr.save()
                    else:
                        prod['quantity_par'] = prod['quantity_par']
                        prod_list.append(int(prod['Product']))
                        irr.save()
                if prod['is_par'] == False:
                    prod_list.append(int(prod['Product']))

            par_entry.save()
            if len(prod_list) == 0:
                irr.is_par = True
                irr.save()
                exit = 'Exit'
                return render(request, 'WISH/par_entry.html', {'exit': exit, 'msg': 'PAR Record (PAR No. - ' + par_entry.par_no + ') is successfully added.'})

            if form.has_changed():
                msg = 0
            else:
                if error == '':
                    msg = 1
                else:
                    msg = 2
            return redirect('WISH.views.par_entry', pk=pk, inv=inv, msg=msg)
    else:
        form = PAR_Form()
        iform = Product_to_PARForm1()
        form.fields['dce'] = forms.ModelChoiceField(Employee.objects.filter(\
            cost_center_no=IRR.objects.get(irr_no=inv).irr_headkey.inv_station_no.cost_center_no.id))
        form.fields['approved_by'] = forms.ModelChoiceField(Employee.objects.filter(\
            cost_center_no=IRR.objects.get(irr_no=inv).irr_headkey.inv_station_no.cost_center_no.id))
        products = IRR.objects.get(irr_no=inv).product
        for prod in products:
            if prod['is_par'] == False:
                prod_list.append(int(prod['Product']))
        iform.fields['product'] = forms.ModelChoiceField(Product.objects.all().filter(id__in=\
            [Product.objects.get(id=p).id for p in prod_list]))
    if int(msg) == 0:
        return render(request, 'WISH/par_entry.html', {'form': form, 'iform': iform, 'msg': 'PAR Record (PAR No. - ' + pk + ') is successfully added.'})
    elif int(msg) == 1 :
        return render(request, 'WISH/par_entry.html', {'form': form, 'iform': iform, 'msg': 'Item is successfully added.'})
    else:
        return render(request, 'WISH/par_entry.html', {'form': form, 'iform': iform, 'error': 'Entered product quantity to be assigned to this employee is greater than stocked items.'})
"""

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

def inv_stat_details(request, pk):
    invs = get_object_or_404(Inventory_stat, inv_station_no=pk)
    return render(request, 'WISH/inv_stat_details.html', {'invs': invs})

def cost_center_details(request, pk):
    cc = get_object_or_404(Cost_center, pk=pk)
    return render(request, 'WISH/cost_center_details.html', {'cc': cc})

def supplier_details(request, pk):
    sup = get_object_or_404(Supplier, supplier_number=pk)
    return render(request, 'WISH/supplier_details.html', {'sup': sup})

def employee_details(request, dce):
    em = get_object_or_404(Employee, dce=dce)
    return render(request, 'WISH/employee_details.html', {'em': em})

def product_form(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm5(request.POST)
        form1 = ProductForm1(request.POST)
        form2 = ProductForm2(request.POST)
        form3 = ProductForm3(request.POST)
        if form1.is_valid() and form2.is_valid() and form3.is_valid():
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
            product.amount = float(form2.data['unit_cost']) * int(form2.data['quantity'])
            product.save()
            return redirect('WISH.views.index')
    else:
        form = ProductForm5(instance=product)
        form1 = ProductForm1()
        form2 = ProductForm2()
        form3 = ProductForm3()
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


def inv_stat_form(request, pk):
    inv = get_object_or_404(Inventory_stat, pk=pk)
    form = Stat_lib(request.POST or None, instance=inv)
    if form.is_valid():
        form.save()
        return redirect('WISH.views.index')
    return render(request, 'WISH/inv_stat_form.html', {'form': form})

def cost_center_form(request, pk):
    cc = get_object_or_404(Cost_center, pk=pk)
    form = CC_lib(request.POST or None, instance=cc)
    if form.is_valid():
        form.save()
        return redirect('WISH.views.index')
    return render(request, 'WISH/cost_center_form.html', {'form': form})

def supplier_form(request, pk):
    sup = get_object_or_404(Supplier, supplier_number=pk)
    form = Supplier_lib(request.POST or None, instance=sup)
    if form.is_valid():
        form.save()
        return redirect('WISH.views.index')
    return render(request, 'WISH/supplier_form.html', {'form': form})

def employee_form(request, dce):
    em = get_object_or_404(Employee, dce=dce)
    form = Employee_lib(request.POST or None, instance=em)
    if form.is_valid():
        form.save()
        return redirect('WISH.views.index')
    return render(request, 'WISH/employee_form.html', {'form': form})

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
        product['pros'] = pro
    return render(request, 'WISH/garv_form.html', {'garvs': garvs, 'products': products})

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

"""def irr_report(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        return redirect('WISH.views.irr_form', pk=q)
    return render(request, 'WISH/irr_report.html', {})

def gatepass_form(request):
    return render(request, 'WISH/gatepass_form.html', {})

def cme_form(request):
    return render(request, 'WISH/cme_form.html', {})

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
    return render(request, 'WISH/garv_report.html', {})"""
