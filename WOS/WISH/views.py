from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
#from random import randint
from .models import *
from .forms import *
import time
import json

# Create your views here.

def index(request):
    if request.user.is_authenticated():
        return render(request, 'WISH/index.html', {})
    else:
        return render(request, 'registration/login1.html')

def aboutus(request):
    return render(request, 'WISH/AboutUs.html', {})

def inv_stat_del(request, pk):
    inv_del = get_object_or_404(Inventory_stat, pk=pk)
    inv_del.is_delete = True
    inv_del.save()
    msg = 'Inventory Station was deleted successfully.'
    try:
        return render(request, 'WISH/index.html', {'msg':msg})
    except:
        return render(request, 'WISH/index.html', {})

def cost_center_del(request, pk):
    cos_del = get_object_or_404(Cost_center, pk=pk)
    cos_del.is_delete = True
    cos_del.save()
    msg = 'Cost center was deleted successfully.'
    try:
        return render(request, 'WISH/index.html', {'msg':msg})
    except:
        return render(request, 'WISH/index.html', {})

def supplier_del(request, pk):
    sup_del = get_object_or_404(Supplier, pk=pk)
    sup_del.is_delete = True
    sup_del.save()
    msg = 'Supplier was deleted successfully.'
    try:
        return render(request, 'WISH/index.html', {'msg':msg})
    except:
        return render(request, 'WISH/index.html', {})

def employee_del(request, pk):
    em_del = get_object_or_404(Employee, pk=pk)
    em_del.is_delete = True
    em_del.save()
    msg = 'Employee was deleted successfully.'
    try:
        return render(request, 'WISH/index.html', {'msg':msg})
    except:
        return render(request, 'WISH/index.html', {})

def file_report(request):
    return render(request, 'WISH/file_report.html', {})


def stat_lib(request):
    if request.method == "POST":
        form = Stat_lib(request.POST)
        if form.is_valid() :
            product = form.save(commit=False)


            product.save()
            msg = 'Inventory Station was added successfully.'

    else:
        form = Stat_lib()
    try:
        form = Stat_lib()
        return render(request, 'WISH/stat_lib.html', {'form': form , 'msg':msg})
    except:
        return render(request, 'WISH/stat_lib.html', {'form': form})

def sup_lib(request):
    if request.method == 'POST':
        form = Sup_lib(request.POST)
        form1 = Sup_lib1(request.POST)
        form2 = Sup_lib2(request.POST)
        if form1.is_valid() and form2.is_valid():
            sup = form.save(commit=False)
            for key in form.data.keys():
                key1 = key
                setattr(sup, key, form1.data[key1])
                setattr(sup, key, form2.data[key1])
            sup.save()
            msg = 'Supplier was added successfully.'
            form = Sup_lib()
            form1 = Sup_lib1()
            form2 = Sup_lib2()
    else:
        form = Sup_lib()
        form1 = Sup_lib1()
        form2 = Sup_lib2()
    try:
        return render(request, 'WISH/sup_lib.html', {'form1': form1, 'form2': form2 , 'msg':msg})
    except:
        return render(request, 'WISH/sup_lib.html', {'form1': form1, 'form2': form2})

def employee_lib(request):
    if request.method == "POST":
        form = Em_lib(request.POST)
        if form.is_valid() :
            employee = form.save(commit=False)
            res = ""
            em_name = list(form.data['name'])
            for name in em_name:

                if name == "'":
                    name = '-'
                    res = res + name
                else:
                    res = res + name
            employee.name = res
            employee.save()
            msg = 'Employee was added successfully.'

    else:
        form = Em_lib()
    try:
        form = Em_lib()
        return render(request, 'WISH/employee_lib.html', {'form': form , 'msg':msg})
    except:
        return render(request, 'WISH/employee_lib.html', {'form': form })

def add_cost_center(request):
    if request.method == "POST":
        form = CC_lib(request.POST)
        if form.is_valid() :
            product = form.save(commit=False)


            product.save()
            msg = 'Cost center was added successfully.'

    else:
        form = CC_lib()

    try:
        form = CC_lib()
        return render(request, 'WISH/add_cost_center.html', {'form': form , 'msg':msg })
    except:
        return render(request, 'WISH/add_cost_center.html', {'form': form })

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

    name = str(request.user.first_name) + ' ' + str(request.user.last_name)

    if request.method == "POST":

        #Forms containing the entries entered by the user
        form = IRR_entryForm(request.POST)
        form1 = IRR_entryForm1(request.POST, name=name)
        form2 = IRR_entryForm2(request.POST, name=name)

        #Non-empty forms are to be validated.
        if form1.is_valid() and form2.is_valid():
            irr_entry = form.save(commit=False)

            #Assignment of values in IRR header model
            for key in form.data.keys():
                key1 = key
                if key == 'supplier' or key == 'inv_station_no' or key == 'dce_user' or key == 'dce_approved':
                    key = key + '_id'
                setattr(irr_entry, key, form1.data[key1])
                setattr(irr_entry, key, form2.data[key1])

            irr_entry.dce_custodian = Employee.objects.get(name=name)
            irr_entry.save()

            return redirect('WISH.views.product_to_irr', pk=irr_entry.pk, inv=int(irr_entry.inv_station_no_id))
    else:
        prodlist = Product.objects.filter(is_irr=False)

        #To check if there are no available products to be made with IRR record
        if len(prodlist) == 0:
            #If true return this exit message
            exit = 'No available products to be made with IRR record.'
        else:
            #else display blank forms.
            form1 = IRR_entryForm1(name=name)
            form2 = IRR_entryForm2(name=name)

    #Rendering of forms
    try:
        return render(request, 'WISH/irr_entry.html', {'exit': exit})
    except:
        return render(request, 'WISH/irr_entry.html', {'form1': form1, 'form2': form2})


prod_to_irr = [] #Product_to_IRR list: List for storing products to be added in a specific IRR form
def product_to_irr(request, pk, inv):
    remove_add = 0
    if request.method == "POST":

        #Forms containing the entries entered by the user
        form = Product_to_IRRForm(request.POST, inv=inv)
        iform = IRR_entry_cont_Form(request.POST, inv=inv)

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
                if 'save' in request.POST:
                    msg = 'IRR record (IRR No. - ' + irr.irr_no + ') was successfully added.'
                    iform = IRR_entry_cont_Form(inv=inv)
                    del prod_to_irr[:]
                    irr.save()
                else:
                    msg = 'Item (' + str(Product.objects.get(id=int(form.data['product'])).item_name) + ') was successfully added.'
            form = Product_to_IRRForm(inv=inv)
    else:
        form = Product_to_IRRForm(inv=inv)
        iform = IRR_entry_cont_Form(inv=inv)

    prodlist = Product.objects.filter(inv_station_no=inv).filter(is_irr=False)
    if len(prodlist) == 0:
        #If true return this exit message
        msg = 'IRR record (IRR No. - ' + str(IRR.objects.latest('wrs_number')) + ') was successfully added.'
        exit = 'No available products to be made with IRR Record.'
    elif len(prodlist) == 1:
        remove_add = 1

    #Rendering of forms and/or messages and/or errors
    try:
        try:
            return render(request, 'WISH/product_to_irr.html', {'exit': exit, 'remove_add': remove_add, 'msg': msg})
        except:
            return render(request, 'WISH/product_to_irr.html', {'form': form, 'iform': iform, 'remove_add': remove_add, 'error': error})
    except:
        try:
            return render(request, 'WISH/product_to_irr.html', {'form': form, 'iform': iform, 'msg': msg, 'remove_add': remove_add, 'pk':pk, 'inv': inv})
        except:
            return render(request, 'WISH/product_to_irr.html', {'form': form, 'iform': iform, 'remove_add': remove_add, 'pk':pk, 'inv': inv})

def miv_entry_S(request, pk):

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
    irrs = IRR.objects.filter(is_miv=False)
    if len(irrs) == 0:
        return render(request, 'WISH/miv_entry_f.html', {'exit':'No IRR Record(s) to be made with MIV Record.'})
    elif len(irrs) <= 10:
        return render(request, 'WISH/miv_entry_f.html',  {'irrs': irrs, 'small_entry': 1})
    else:
        return render(request, 'WISH/miv_entry_f.html', {'irrs':irrs})

def par_f(request):
    irrs = IRR.objects.filter(is_par=False)
    if len(irrs) == 0:
        return render(request, 'WISH/par_f.html', {'exit': 'No IRR Record(s) to be made with PAR Record.'})
    elif len(irrs) <= 10:
        return render(request, 'WISH/par_f.html',  {'irrs': irrs, 'small_entry': 1})
    else:
        return render(request, 'WISH/par_f.html', {'irrs':irrs})

def garv_entry_f(request):
    pars = PAR.objects.filter(is_garv=False)
    if len(pars) == 0:
        return render(request, 'WISH/garv_entry_f.html', {'exit': 'No PAR Record(s) to be made with GARV Record.'})
    elif len(pars) <= 10:
        return render(request, 'WISH/garv_entry_f.html',  {'pars': pars, 'small_entry': 1})
    else:
        return render(request, 'WISH/garv_entry_f.html', {'pars':pars})

prod_to_garv = []
def product_to_garv(request, pk):
    prod_list = []
    error = ''
    msg = 3
    remove_add = 0
    products = PAR.objects.get(par_no=pk)
    for prod in products.product:
        if prod['is_garv'] == False:
            prod_list.append(int(prod['Product']))
    try:
        garv_no = int(GARV.objects.latest('garv_date').garv_no)
    except:
        garv_no = 0
    if request.method == "POST":
        form = GARV_entryForm(request.POST, pk=pk)
        if garv_no == 0:
            iform = Product_to_GARVform(request.POST, prodlist=prod_list)
        else:
            iform = Product_to_GARVform1(request.POST, prodlist=prod_list)

        if form.is_valid():
            garv = form.save(commit=False)

            try:
                garv.garv_no = iform.data['garv_no']
                garv_no = garv.garv_no
            except:
                garv.garv_no = garv_no

            for prod in products.product:
                if prod['Product'] == str(iform.data['product']):
                    prod['quantity_garv'] = int(prod['quantity_garv']) - int(iform.data['quantity'])
                    if int(prod['quantity_garv']) < 0:
                        error = 'Entered quantity is greater than accepted items.'
                    elif int(prod['quantity_garv']) == 0:
                        prod['quantity_garv'] = 0
                        prod['is_garv'] = True
                        prod_list.remove(int(prod['Product']))
                        products.save()
                    else:
                        prod['quantity_garv'] = prod['quantity_garv']
                        prod_list.append(int(prod['Product']))
                        products.save()
                if prod['is_garv'] == False:
                    prod_list.append(int(prod['Product']))

            if error == '':
                prod_to_garv.append({'Product': iform.data['product'], 'Quantity': \
                    iform.data['quantity'], 'PAR_number': pk, 'Remarks': \
                    iform.data['remarks']})

                p = Product.objects.get(id=int(iform.data['product']))
                p.quantity = int(p.quantity) + int(prod['Quantity'])
                p.save()

                garv.garv_date = time.strftime("%Y-%m-%d")
                garv.dce = (PAR.objects.get(par_no=pk)).dce
                garv.wo_number = (PAR.objects.get(par_no=pk)).wo_number
                res = json.dumps(prod_to_garv)
                garv.product_to_GARV = res

                garv.save()
                if len(prod_list) == 0:
                    products.is_garv = True
                    products.save()
                    del prod_to_garv[:]
                    exit = 'Exit'
                    return render(request, 'WISH/par_entry.html', {'exit': exit, 'msg': 'GARV Record (GARV No. - ' + str(garv.garv_no) + ') is successfully added.'})

                if 'save' in request.POST:
                    msg = 0
                    del prod_to_par[:]
                    form = GARV_entryForm(pk=pk)
                    iform = Product_to_GARVform(prodlist=prod_list)
                else:
                    msg = 1
                    if garv_no == 0:
                        if len(prod_list) == 1:
                            remove_add = 1
                        iform = Product_to_GARVform(prodlist=prod_list)
                    else:
                        if len(prod_list) == 1:
                            remove_add = 1
                        iform = Product_to_GARVform1(prodlist=prod_list)
            else:
                msg = 2

    else:
        form = GARV_entryForm(pk=pk)
        iform = Product_to_GARVform(prodlist=prod_list)

    if len(prod_list) == 1:
        remove_add = 1

    if int(msg) == 0:
        return render(request, 'WISH/garv_entry.html', {'form': form, 'iform': iform, 'remove_add': remove_add, 'msg': 'PAR Record (PAR No. - ' + str(par_no) + ') is successfully added.'})
    elif int(msg) == 1:
        return render(request, 'WISH/garv_entry.html', {'form': form, 'iform': iform, 'remove_add': remove_add, 'msg': 'Item is successfully added.'})
    elif int(msg) == 2:
        return render(request, 'WISH/garv_entry.html', {'form': form, 'iform': iform, 'remove_add': remove_add, 'error': 'Entered product quantity to be assigned to this employee is greater than stocked items.'})
    else:
        return render(request, 'WISH/garv_entry.html', {'form': form, 'iform': iform, 'remove_add': remove_add})

prod_to_par = []
def par(request, inv):
    prod_list = []
    error = ''
    msg = 3
    remove_add = 0
    products = IRR.objects.get(irr_no=inv)
    for prod in products.product:
        if prod['is_par'] == False:
            prod_list.append(int(prod['Product']))
    try:
        par_no = int(PAR.objects.latest('date_acquired').par_no)
    except:
        par_no = 0
    if request.method == "POST":
        form = PAR_Form(request.POST, inv=inv)
        if par_no == 0:
            iform = Product_to_PARForm(request.POST, prodlist=prod_list)
        else:
            iform = Product_to_PARForm1(request.POST, prodlist=prod_list)

        if form.is_valid() and iform.is_valid():
            par_entry = form.save(commit=False)

            try:
                par_entry.par_no = iform.data['par_no']
                par_no = par_entry.par_no
            except:
                par_entry.par_no = par_no

            for prod in products.product:
                if prod['Product'] == str(iform.data['product']):
                    prod['quantity_par'] = int(prod['quantity_par']) - int(iform.data['quantity'])
                    if int(prod['quantity_par']) < 0:
                        error = 'Entered quantity is greater than stocked items.'
                    elif int(prod['quantity_par']) == 0:
                        prod['quantity_par'] = 0
                        prod['is_par'] = True
                        prod_list.remove(int(prod['Product']))
                        products.save()
                    else:
                        prod['quantity_par'] = prod['quantity_par']
                        products.save()

            if error == '':
                par_entry.wo_number = IRR.objects.get(irr_no=inv)
                par_entry.par_date = time.strftime("%Y-%m-%d")
                prod_to_par.append({'Product': iform.data['product'],\
                                'Quantity': iform.data['quantity'], 'quantity_garv': iform.data['quantity'],\
                                'is_garv': False})
                par_entry.amt_cost = 0
                for product in prod_to_par:
                    pro = Product.objects.get(id=product['Product'])
                    amount = float(product['Quantity']) * int(pro.unit_cost)
                    par_entry.amt_cost = par_entry.amt_cost + amount

                res = json.dumps(prod_to_par)
                par_entry.product = prod_to_par
                par_entry.inv_stat_no_id = IRR.objects.get(irr_no=inv).irr_headkey.inv_station_no.id

                par_entry.issued_by = Employee.objects.get(name=(str(request.user.first_name) + ' ' + str(request.user.last_name)))

                par_entry.save()
                if len(prod_list) == 0:
                    products.is_par = True
                    products.save()
                    del prod_to_par[:]
                    exit = 'Exit'
                    return render(request, 'WISH/par_entry.html', {'exit': exit, 'msg': 'PAR Record (PAR No. - ' + str(par_entry.par_no) + ') is successfully added.'})

                if 'save' in request.POST:
                    msg = 0
                    del prod_to_par[:]
                    form = PAR_Form(inv=inv)
                    iform = Product_to_PARForm(prodlist=prod_list)
                else:
                    msg = 1
                    if par_no == 0:
                        iform = Product_to_PARForm(prodlist=prod_list)
                    else:
                        iform = Product_to_PARForm1(prodlist=prod_list)
            else:
                msg = 2
    else:
        form = PAR_Form(inv=inv)
        iform = Product_to_PARForm(prodlist=prod_list)

    if len(prod_list) == 1:
        remove_add = 1

    if int(msg) == 0:
        return render(request, 'WISH/par_entry.html', {'form': form, 'iform': iform, 'remove_add': remove_add, 'msg': 'PAR Record (PAR No. - ' + str(par_no) + ') is successfully added.'})
    elif int(msg) == 1:
        return render(request, 'WISH/par_entry.html', {'form': form, 'iform': iform, 'remove_add': remove_add, 'msg': 'Item is successfully added.'})
    elif int(msg) == 2:
        return render(request, 'WISH/par_entry.html', {'form': form, 'iform': iform, 'remove_add': remove_add, 'error': 'Entered product quantity to be assigned to this employee is greater than stocked items.'})
    else:
        return render(request, 'WISH/par_entry.html', {'form': form, 'iform': iform, 'remove_add': remove_add})


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
        msg = 'Inventory Station was editted successfully.'
    try:
        form = Stat_lib(request.POST or None, instance=inv)
        return render(request, 'WISH/inv_stat_form.html', {'form': form, 'msg':msg})
    except:
        return render(request, 'WISH/inv_stat_form.html', {'form': form})

def cost_center_form(request, pk):
    cc = get_object_or_404(Cost_center, pk=pk)
    form = CC_lib(request.POST or None, instance=cc)
    if form.is_valid():
        form.save()
        msg = 'Cost center was editted successfully.'
    try:
        form = CC_lib(request.POST or None, instance=cc)
        return render(request, 'WISH/cost_center_form.html', {'form': form, 'msg':msg})
    except:
        return render(request, 'WISH/cost_center_form.html', {'form': form})

def supplier_form(request, pk):
    sup = get_object_or_404(Supplier, supplier_number=pk)
    if request.method == 'POST':
        form = Supplier_lib(request.POST)
        form1 = Supplier_lib1(request.POST)
        form2 = Supplier_lib2(request.POST)
        if form1.is_valid() and form2.is_valid():
            for key in form.data.keys():
                key1 = key
                setattr(sup, key, form1.data[key1])
                setattr(sup, key, form2.data[key1])
            sup.save()
            msg = 'Supplier information was editted successfully.'
    else:
        form = Supplier_lib(instance=sup)
        form1 = Supplier_lib1()
        form2 = Supplier_lib2()
        for key in form.fields.keys():
            for key1 in form1.fields.keys():
                if key == key1:
                    form1.fields[key].initial = getattr(sup, key)
            for key2 in form2.fields.keys():
                if key == key2:
                    form2.fields[key].initial = getattr(sup, key)
    try:
        form = Supplier_lib(instance=sup)
        form1 = Supplier_lib1()
        form2 = Supplier_lib2()
        for key in form.fields.keys():
            for key1 in form1.fields.keys():
                if key == key1:
                    form1.fields[key].initial = getattr(sup, key)
            for key2 in form2.fields.keys():
                if key == key2:
                    form2.fields[key].initial = getattr(sup, key)
        return render(request, 'WISH/supplier_form.html', {'form1': form1, 'form2': form2, 'msg':msg})
    except:
        return render(request, 'WISH/supplier_form.html', {'form1': form1, 'form2': form2})

def employee_form(request, dce):
    em = get_object_or_404(Employee, dce=dce)
    form = Employee_lib(request.POST or None, instance=em)
    if form.is_valid():
        form.save()
        msg = 'Employee information was editted successfully.'
    try:
        form = Employee_lib(request.POST or None, instance=em)
        return render(request, 'WISH/employee_form.html', {'form': form, 'msg':msg})
    except:
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
