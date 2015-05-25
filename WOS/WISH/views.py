# Create your views here.
# pylint: disable=bare-except,invalid-name, too-many-branches, unused-variable, too-many-statements, too-many-locals

"""views"""
from django.shortcuts import render, redirect, get_object_or_404
from WISH.models import Supplier, Product, PAR, GARV, CostCenter, \
        InventoryStat, Employee, IRR, MIV
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from WISH import forms
import time
import json

prod_to_par = []
prod_to_irr = []
prod_to_garv = []

def log_in(request):
    """function"""
    if request.method == 'POST':
        if 'signup' in request.POST:
            form1 = forms.SignUpForm(request.POST or None)
            form = forms.LoginForm(request.POST or None)
            if form1.is_valid():
                dce = form1.data['dce']
                emp = Employee.objects.get(dce=dce)
                if emp.position == "Property Custodian":
                    try:
                        user = User.objects.create_superuser(username=form1.data\
                        ['username1'], first_name=form1.data['first_name'],
                        last_name=form1.data['last_name'], password=\
                        form1.data['password1'], email=None)

                        emp.user_id_id = user.id
                        emp.save()
                        form = forms.LoginForm()
                        form1 = forms.SignUpForm()
                        return render(request, 'WISH/login.html', {'form':form, \
                         'form1': form1, 'msg': "You've successfully created an account."})
                    except:
                        form = forms.LoginForm()
                        return render(request, 'WISH/login.html', \
                        {'error1': 'Username already exists.',\
                         'form':form, 'form1': form1})
                else:
                    form = forms.LoginForm()
                    return render(request, 'WISH/login.html', \
                        {'error1': 'Does not match any custodian profile.',\
                         'form':form, 'form1': form1})
        elif 'login' in request.POST:
            form1 = forms.SignUpForm(request.POST or None)
            form = forms.LoginForm(request.POST or None)
            if form.is_valid():
                user = authenticate(username=form.data['username'], \
                    password=form.data['password'])
                if user is not None:
                    login(request, user)
                    form = forms.LoginForm()
                    form1 = forms.SignUpForm()
                    return redirect('index')
                else:
                    form1 = forms.SignUpForm()
                    return render(request, 'WISH/login.html', \
                        {'error': 'Username and password does not match.',\
                         'form':form, 'form1': form1})
    else:
        form = forms.LoginForm()
        form1 = forms.SignUpForm()
        return render(request, 'WISH/login.html', {'form': form, 'form1': form1})

def log_out(request):
    """function"""
    logout(request)
    form = forms.LoginForm()
    form1 = forms.SignUpForm()
    return render(request, 'WISH/login.html', {'form': form, 'form1': form1})

def index(request):
    """function"""
    try:
        product = Product.objects.order_by('id')[:3]
    except:
        product = []
    try:
        irr = IRR.objects.latest('wrs_number')
    except:
        irr = []
    try:
        par = PAR.objects.latest('par_no')
    except:
        par = []
    try:
        garv = GARV.objects.latest('garv_no')
    except:
        garv = []
    try:
        inv = InventoryStat.objects.latest('id')
    except:
        inv = []
    try:
        sup = Supplier.objects.latest('id')
    except:
        sup = []
    try:
        cc = CostCenter.objects.latest('id')
    except:
        cc = []
    return render(request, 'WISH/index.html', {'product': product, 'irr': irr, \
    'par': par, 'garv': garv, 'inv': inv, 'sup': sup, 'cc': cc})

def guest(request):
    """function"""
    return render(request, 'WISH/index.html', {})

def aboutus(request):
    """function"""
    return render(request, 'WISH/AboutUs.html', {})

def inv_stat_del(request, pk):
    """function"""
    inv_del = get_object_or_404(InventoryStat, pk=pk)
    inv_del.is_delete = True
    inv_del.save()
    return render(request, 'WISH/index.html', {'msg':'Inventory Station' + \
        ' was deleted successfully.'})

def cost_center_del(request, pk):
    """function"""
    cos_del = get_object_or_404(CostCenter, pk=pk)
    cos_del.is_delete = True
    cos_del.save()
    return render(request, 'WISH/index.html', {'msg':'Cost center' + \
        ' was deleted successfully.'})

def supplier_del(request, pk):
    """function"""
    sup_del = get_object_or_404(Supplier, pk=pk)
    sup_del.is_delete = True
    sup_del.save()
    return render(request, 'WISH/index.html', {'msg':'Supplier' + \
        ' was deleted successfully.'})

def employee_del(request, pk):
    """function"""
    em_del = get_object_or_404(Employee, pk=pk)
    em_del.is_delete = True
    em_del.save()
    try:
        return render(request, 'WISH/index.html', {'msg':'Employee' + \
        ' was deleted successfully.'})
    except:
        return render(request, 'WISH/index.html', {})

def add_supplier(request):
    """function"""
    if request.method == 'POST':
        form = forms.Suplib(request.POST)
        form1 = forms.Suplib1(request.POST)
        form2 = forms.Suplib2(request.POST)
        if form1.is_valid() and form2.is_valid():
            sup = form.save(commit=False)

            for key in form.data.keys():
                key1 = key
                setattr(sup, key, form1.data[key1])
                setattr(sup, key, form2.data[key1])

            res = ""
            sup_name = list(form.data['supplier_name'])
            for name in sup_name:
                if name == "'":
                    name = '-'
                    res = res + name
                else:
                    res = res + name
            sup.supplier_name = res

            sup.save()
            msg = 'Supplier was added successfully.'
            form = forms.Suplib()
            form1 = forms.Suplib1()
            form2 = forms.Suplib2()
            return render(request, 'WISH/add_supplier.html', \
              {'form1': form1, 'form2': form2, 'msg':'Supplier ' +\
              'was added successfully.'})
    else:
        form = forms.Suplib()
        form1 = forms.Suplib1()
        form2 = forms.Suplib2()
    return render(request, 'WISH/add_supplier.html', \
        {'form1': form1, 'form2': form2})

def add_employee(request):
    """function"""
    if request.method == "POST":
        form = forms.Emlib(request.POST)
        if form.is_valid():
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
            form = forms.Emlib()
            return render(request, 'WISH/add_employee.html', {'form': form,\
                'msg':'Employee was added successfully.'})
    else:
        form = forms.Emlib()

    return render(request, 'WISH/add_employee.html', {'form': form})

def product_new(request):
    """function"""
    if request.method == "POST":

        #Forms containing the entries entered by the user
        form = forms.ProductForm(request.POST)
        form1 = forms.ProductForm1(request.POST)
        form2 = forms.ProductForm2(request.POST)
        form3 = forms.ProductForm3(request.POST)

        #Non-empty forms are to be validated.
        if form.is_valid() and form1.is_valid() \
        and form2.is_valid():

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

            product.amount = int(form2.data['unit_cost']) * \
                int(form2.data['quantity'])
            product.save()

            #Displaying of blank forms
            form1 = forms.ProductForm1()
            form2 = forms.ProductForm2()
            form3 = forms.ProductForm3()

            return render(request, 'WISH/product_add.html', {'form3': form3,\
             'form1':form1, 'form2': form2, 'msg': 'Product (' + \
             product.item_name + ') was added successfully.'})
    else:
        #Displaying of blank forms
        form = forms.ProductForm()
        form1 = forms.ProductForm1()
        form2 = forms.ProductForm2()
        form3 = forms.ProductForm3()

    #Rendering of forms and/or messages
    return render(request, 'WISH/product_add.html', {'form3': form3, \
            'form1':form1, 'form2': form2})

def irr_entry(request):
    """function"""

    name = str(request.user.first_name) + ' ' + str(request.user.last_name)

    if request.method == "POST":

        #Forms containing the entries entered by the user
        form = forms.IRRentryForm(request.POST)
        form1 = forms.IRRentryForm1(request.POST, name=name)
        form2 = forms.IRRentryForm2(request.POST, name=name)

        #Non-empty forms are to be validated.
        if form1.is_valid() and form2.is_valid():
            irr_entry = form.save(commit=False)

            #Assignment of values in IRR header model
            for key in form.data.keys():
                key1 = key
                if key == 'supplier' or key == 'inv_station_no' \
                or key == 'dce_user' or key == 'dce_approved':
                    key = key + '_id'
                setattr(irr_entry, key, form1.data[key1])
                setattr(irr_entry, key, form2.data[key1])

            irr_entry.dce_custodian = Employee.objects.get(name=name)
            irr_entry.save()

            return redirect('new_irr_cont',\
             pk=irr_entry.pk, inv=int(irr_entry.inv_station_no_id))
    else:
        prodlist = Product.objects.filter(is_irr=False)

        if len(prodlist) == 0:
            #If true return this exit message
            return render(request, 'WISH/irr_entry.html',\
              {'exit': 'No available products to be made with IRR record.'})
        else:
            #else display blank forms.
            form1 = forms.IRRentryForm1(name=name)
            form2 = forms.IRRentryForm2(name=name)
            return render(request, 'WISH/irr_entry.html',\
                {'form1': form1, 'form2': form2})

def product_to_irr(request, pk, inv):
    """function"""
    remove_add = 0
    if request.method == "POST":

        #Forms containing the entries entered by the user
        form = forms.ProducttoIRRForm(request.POST, inv=inv)
        iform = forms.IRRentrycontForm(request.POST, inv=inv)

        if 'delete' in request.POST:
            k = int(request.POST['delete'])
            prod = Product.objects.get(id=prod_to_irr[k]['Product'])
            prod.is_irr = False
            prod.save()
            prod_to_irr.remove(prod_to_irr[k])

        #Non-empty forms are to be validated.
        elif form.is_valid() and iform.is_valid():

            #To check if quantity accepted entered is
                #less than the present stocked items.
            if Product.objects.get(id=int(form.data['product'])).quantity \
            < int(form.data['quantity_accepted']):
                return render(request, 'WISH/product_to_irr.html', \
                {'form': form, 'iform': iform, 'remove_add': \
                remove_add, 'error': 'Accepted quantity is greater than ' + \
                'the number of stocked items.', 'product': prod_to_irr})

            else:
                #Storing of products for this specific IRR form.
                prod_to_irr.append({'Product': form.data['product'], \
                    'quantity_accepted': int(form.data['quantity_accepted']), \
                    'quantity_rejected':int(form.data['quantity_rejected']), \
                    'quantity_balance': int(form.data['quantity_balance']), \
                    'is_par':False, 'quantity_par': int(form.data['quantity_accepted'])})

                p = Product.objects.get(id=int(form.data['product']))
                p.quantity = int(form.data['quantity_accepted'])
                p.balance = int(form.data['quantity_balance'])
                p.is_irr = True

                irr = iform.save(commit=False)

                #Generation of IRR number
                if len(IRR.objects.all()) != 0:
                    no = int((IRR.objects.latest\
                        ('wrs_number')).irr_no) + 1
                    irr.irr_no = str(no)
                    if (6-len(irr.irr_no)) > 0:
                        for i in range(6-len(irr.irr_no)):
                            irr.irr_no = '0' + irr.irr_no
                else:
                    irr.irr_no = '000000'

                irr.irr_headkey_id = pk

                #Generation of WRS number
                if len(IRR.objects.all()) != 0:
                    no = int((IRR.objects.latest\
                        ('wrs_number')).wrs_number) + 1
                    irr.wrs_number = str(no)
                else:
                    irr.wrs_number = irr.irr_headkey.\
                    inv_station_no.inv_station_no + '000000'

                for prod in prod_to_irr:
                    if 'pros' in prod:
                        del prod['pros']

                irr.product = json.dumps(prod_to_irr)

                #To check if all entries for the IRR form is filled.
                if 'save' in request.POST:
                    msg = 'IRR record (IRR No. - ' + \
                        irr.irr_no + ') was successfully added.'
                    iform = forms.IRRentrycontForm(inv=inv)
                    del prod_to_irr[:]
                    irr.save()
                    p.save()
                else:
                    msg = 'Item (' + str(Product.objects.\
                        get(id=int(form.data['product'])).\
                        item_name) + ') was successfully added.'
                    p.save()
                    for prod in prod_to_irr:
                        pro = Product.objects.get(id=prod['Product'])
                        prod['pros'] = pro
        form = forms.ProducttoIRRForm(inv=inv)
    else:
        form = forms.ProducttoIRRForm(inv=inv)
        iform = forms.IRRentrycontForm(inv=inv)

    prodlist = Product.objects.filter(inv_station_no=inv).\
    filter(is_irr=False)
    if len(prodlist) == 0:
        #If true return this exit message
        msg = 'IRR record (IRR No. - ' + str(IRR.objects.latest\
            ('wrs_number')) + ') was successfully added.'
        exit = 'No available products to be made with IRR Record.'
    elif len(prodlist) == 1:
        remove_add = 1

    #Rendering of forms and/or messages and/or errors
    try:
        return render(request, 'WISH/product_to_irr.html', \
            {'exit': exit, 'remove_add': remove_add, 'msg': msg})
    except:
        try:
            return render(request, 'WISH/product_to_irr.html', \
                {'form': form, 'iform': iform, 'msg': msg, \
                'remove_add': remove_add, 'product': prod_to_irr})
        except:
            return render(request, 'WISH/product_to_irr.html', \
                {'form': form, 'iform': iform, 'remove_add': \
                remove_add, 'product': prod_to_irr})

def miv_entry_S(request, pk):
    """function"""
    if request.method == "POST":
        #Forms containing the entries entered by the user
        form = forms.MIVentryForm(request.POST)

        #Non-empty forms are to be validated.
        if form.is_valid():

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

            #Deducting the number of quantities to be pulled out by the user
            for prod in miv_entry.irr_no.product:
                p = Product.objects.get(id=(prod['Product']))
                p.quantity = int(p.quantity) - \
                int(prod['quantity_accepted'])
                p.amount = int(p.unit_cost) * int(p.quantity)
                p.average_amount = p.amount
                p.save()

            miv_entry.save()

            IRR.objects.get(irr_no=pk).is_miv = True
            IRR.objects.get(irr_no=pk).save()

            return render(request, 'WISH/miv_entry.html', \
                {'msg': 'MIV record (MIV No. - ' + miv_entry.miv_no \
                + ') was successfully added.', 'exit': 'Exit'})

    else:
        form = forms.MIVentryForm()

    return render(request, 'WISH/miv_entry.html', {'form': form})

def miv_entry(request):
    """function"""
    irrs = IRR.objects.filter(is_miv=False)
    if len(irrs) == 0:
        return render(request, 'WISH/miv_entry_f.html', \
            {'exit':'No IRR Record(s) to be made with MIV Record.'})
    elif len(irrs) <= 10:
        return render(request, 'WISH/miv_entry_f.html', \
            {'irrs': irrs, 'small_entry': 1})
    else:
        return render(request, 'WISH/miv_entry_f.html', {'irrs':irrs})

def par_f(request):
    """function"""
    irrs = IRR.objects.filter(is_par=False)
    if len(irrs) == 0:
        return render(request, 'WISH/par_f.html', \
            {'exit': 'No IRR Record(s) to be made with PAR Record.'})
    elif len(irrs) <= 10:
        return render(request, 'WISH/par_f.html', \
            {'irrs': irrs, 'small_entry': 1})
    else:
        return render(request, 'WISH/par_f.html', {'irrs':irrs})

def garv_entry_f(request):
    """function"""
    pars = PAR.objects.filter(is_garv=False)
    if len(pars) == 0:
        return render(request, 'WISH/garv_entry_f.html', \
            {'exit': 'No PAR Record(s) to be made with GARV Record.'})
    elif len(pars) <= 10:
        return render(request, 'WISH/garv_entry_f.html', \
            {'pars': pars, 'small_entry': 1})
    else:
        return render(request, 'WISH/garv_entry_f.html', {'pars':pars})

def product_to_garv(request, pk):
    """function"""
    prod_list = []
    msg = 2
    remove_add = 0
    products = PAR.objects.get(par_no=pk)
    for prod in products.product:
        if prod['is_garv'] == False:
            prod_list.append(int(prod['Product']))
    if request.method == "POST":
        form = forms.GARVentryForm(request.POST, pk=pk)
        iform = forms.ProducttoGARVform(request.POST, prodlist=prod_list)

        if 'delete' in request.POST:
            k = int(request.POST['delete'])
            for prod in products.product:
                if prod['Product'] == prod_to_garv[k]['Product']:
                    prod['quantity_garv'] = prod_to_garv[k]['Quantity']
                    prod['is_garv'] = False
                    prod_list.append(int(prod['Product']))
            products.is_par = False
            products.save()
            prod_to_garv.remove(prod_to_garv[k])
            iform = forms.ProducttoGARVform(prodlist=prod_list)

        elif form.is_valid() and iform.is_valid():
            garv = form.save(commit=False)

            garv_no = form.data['garv_no']

            for prod in products.product:
                if prod['Product'] == str(iform.data['product']):
                    prod['quantity_garv'] = int(prod['quantity_garv']) - \
                    int(iform.data['quantity'])
                    if int(prod['quantity_garv']) < 0:
                        return render(request, 'WISH/garv_entry.html',\
                         {'form': form, \
                        'iform': iform, 'remove_add': remove_add, 'error': \
                        'Entered product quantity to be returned is greater ' +\
                        'than stocked items.', 'product': prod_to_garv})
                    elif int(prod['quantity_garv']) == 0:
                        prod['quantity_garv'] = 0
                        prod['is_garv'] = True
                        prod_list.remove(int(prod['Product']))
                        products.save()
                    else:
                        prod['quantity_garv'] = prod['quantity_garv']
            prod_to_garv.append({'Product': iform.data['product'],\
             'Quantity': iform.data['quantity'], 'PAR_number': \
             pk, 'Remarks': iform.data['remarks']})

            p = Product.objects.get(id=int(iform.data['product']))
            p.quantity = int(p.quantity) + int(prod['Quantity'])
            p.save()

            garv.garv_date = time.strftime("%Y-%m-%d")
            garv.dce = (PAR.objects.get(par_no=pk)).dce
            garv.wo_number = (PAR.objects.get(par_no=pk)).wo_number

            for prod in prod_to_garv:
                if 'pros' in prod:
                    del prod['pros']

            garv.product_to_GARV = json.dumps(prod_to_garv)
            garv.confirmed_by = Employee.objects.get\
            (name=(str(request.user.first_name) + ' ' + \
                str(request.user.last_name)))

            if len(prod_list) == 0:
                products.is_garv = True
                products.save()
                garv.save()
                del prod_to_garv[:]
                return render(request, 'WISH/garv_entry.html', \
                    {'exit': 'Exit', 'msg': 'GARV Record (GARV No. - ' +\
                     str(garv_no) + ') is successfully added.'})

            if 'save' in request.POST:
                msg = 0
                garv.save()
                del prod_to_garv[:]
                form = forms.GARVentryForm(pk=pk)
                iform = forms.ProducttoGARVform(prodlist=prod_list)
            else:
                msg = 1
                products.save()
                iform = forms.ProducttoGARVform(prodlist=prod_list)
                for prod in prod_to_garv:
                    pro = Product.objects.get(id=int(prod['Product']))
                    prod['pros'] = pro
            iform = forms.ProducttoGARVform(prodlist=prod_list)

    else:
        form = forms.GARVentryForm(pk=pk)
        iform = forms.ProducttoGARVform(prodlist=prod_list)

    if len(prod_list) == 1:
        remove_add = 1

    if int(msg) == 0:
        return render(request, 'WISH/garv_entry.html', {'form': form, \
            'iform': iform, 'remove_add': remove_add, 'msg': \
            'GARV Record (GARV No. - ' + str(garv_no) + \
            ') is successfully added.'})
    elif int(msg) == 1:
        return render(request, 'WISH/garv_entry.html', {'form': form, \
            'iform': iform, 'remove_add': remove_add, 'msg': \
            'Item is successfully added.', 'product': prod_to_garv})
    else:
        return render(request, 'WISH/garv_entry.html', {'form': form, \
            'iform': iform, 'remove_add': remove_add, 'product': prod_to_garv})

def par(request, inv):
    """function"""
    prod_list = []
    msg = 2
    remove_add = 0
    products = IRR.objects.get(irr_no=inv)
    for prod in products.product:
        if prod['is_par'] == False:
            prod_list.append(int(prod['Product']))
    if request.method == "POST":
        form = forms.PARForm(request.POST, inv=inv)
        iform = forms.ProducttoPARForm(request.POST, prodlist=prod_list)

        if 'delete' in request.POST:
            k = int(request.POST['delete'])
            for prod in products.product:
                if prod['Product'] == prod_to_par[k]['Product']:
                    prod['quantity_par'] = prod_to_par[k]['Quantity']
                    prod['is_par'] = False
                    prod_list.append(int(prod['Product']))
            products.is_par = False
            products.save()
            prod_to_par.remove(prod_to_par[k])
            iform = forms.ProducttoPARForm(prodlist=prod_list)

        elif form.is_valid() and iform.is_valid():
            par_entry = form.save(commit=False)

            par_no = form.data['par_no']

            for prod in products.product:
                if prod['Product'] == str(iform.data['product']):
                    prod['quantity_par'] = int(prod['quantity_par'])\
                     - int(iform.data['quantity'])
                    if int(prod['quantity_par']) < 0:
                        return render(request, 'WISH/par_entry.html', \
                            {'form': form,\
                        'iform': iform, 'remove_add': remove_add, 'error': \
                        'Entered product quantity to be assigned to this ' +\
                        'employee is greater than stocked items.', 'product': \
                        prod_to_par})
                    elif int(prod['quantity_par']) == 0:
                        prod['quantity_par'] = 0
                        prod['is_par'] = True
                        prod_list.remove(int(prod['Product']))
                        products.save()
                    else:
                        prod['quantity_par'] = prod['quantity_par']

            par_entry.wo_number = IRR.objects.get(irr_no=inv)
            par_entry.par_date = time.strftime("%Y-%m-%d")
            prod_to_par.append({'Product': iform.data['product'], 'Quantity':\
             iform.data['quantity'], 'quantity_garv': iform.data['quantity'],\
             'is_garv': False})

            par_entry.amt_cost = 0
            for product in prod_to_par:
                pro = Product.objects.get(id=product['Product'])
                amount = float(product['Quantity']) * \
                int(pro.unit_cost)
                par_entry.amt_cost = par_entry.amt_cost + amount
                if 'pros' in prod:
                    del prod['pros']
            
            par_entry.product = json.dumps(prod_to_par)
            par_entry.inv_stat_no_id = IRR.objects.get(irr_no=inv).\
            irr_headkey.inv_station_no.id

            par_entry.issued_by = Employee.objects.get\
            (name=(str(request.user.first_name) + ' ' + \
                str(request.user.last_name)))

            if len(prod_list) == 0:
                products.is_par = True
                products.save()
                par_entry.save()
                del prod_to_par[:]
                return render(request, 'WISH/par_entry.html', \
                 {'exit': 'Exit', 'msg': 'PAR Record (PAR No. - '\
                 + str(par_no) + ') is successfully added.'})

            if 'save' in request.POST:
                msg = 0
                par_entry.save()
                products.save()
                del prod_to_par[:]
                form = forms.PARForm(inv=inv)
            else:
                msg = 1
                products.save()
                iform = forms.ProducttoPARForm(prodlist=prod_list)
                for prod in prod_to_par:
                    pro = Product.objects.get(id=int(prod['Product']))
                    prod['pros'] = pro
            iform = forms.ProducttoPARForm(prodlist=prod_list)

    else:
        form = forms.PARForm(inv=inv)
        iform = forms.ProducttoPARForm(prodlist=prod_list)

    if len(prod_list) == 1:
        remove_add = 1

    if int(msg) == 0:
        return render(request, 'WISH/par_entry.html', \
            {'form': form, 'iform': iform, 'remove_add': remove_add, \
            'msg': 'PAR Record (PAR No. - ' + str(par_no) + ') \
            is successfully added.'})
    elif int(msg) == 1:
        return render(request, 'WISH/par_entry.html', \
            {'form': form, 'iform': iform, 'remove_add': remove_add, \
            'msg': 'Item is successfully added.', 'product': prod_to_par})
    else:
        return render(request, 'WISH/par_entry.html', {'form': form, \
            'iform': iform, 'remove_add': remove_add, 'product': prod_to_par})

def product_form(request, pk):
    """function"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = forms.ProductForm5(request.POST)
        form1 = forms.ProductForm1(request.POST)
        form2 = forms.ProductForm2(request.POST)
        form3 = forms.ProductForm3(request.POST)
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
            if int(form2.data['quantity']) > 1 and \
            not (product.unit_measure.endswith('s')):
                if form2.data['unit_measure'] == 'box':
                    product.unit_measure = str(product.unit_measure) + 'es'
                else:
                    product.unit_measure = str(product.unit_measure) + 's'
            if int(form2.data['quantity']) == 1 and (product.unit_measure.endswith('s')):
                if product.unit_measure.startswith('b'):
                    product.unit_measure = product.unit_measure[:-2]
                else:
                    product.unit_measure = product.unit_measure[:-1]

            product.amount = float(form2.data['unit_cost']) * \
            float(form2.data['quantity'])
            product.save()
        return redirect('prod_details', pk=pk)
    else:
        form = forms.ProductForm5(instance=product)
        form1 = forms.ProductForm1()
        form2 = forms.ProductForm2()
        form3 = forms.ProductForm3()
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
    return render(request, 'WISH/product_form.html', {'form1': form1, \
        'form2': form2, 'form3': form3})

def supplier_form(request, pk):
    """function"""
    sup = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = forms.Supplierlib(request.POST)
        form1 = forms.Supplierlib1(request.POST)
        form2 = forms.Supplierlib2(request.POST)
        if form1.is_valid() and form2.is_valid():
            for key in form.data.keys():
                key1 = key
                setattr(sup, key, form1.data[key1])
                setattr(sup, key, form2.data[key1])
            sup.save()
            return redirect('supplier_details', pk=pk)
    else:
        form = forms.Supplierlib(instance=sup)
        form1 = forms.Supplierlib1()
        form2 = forms.Supplierlib2()
        for key in form.fields.keys():
            for key1 in form1.fields.keys():
                if key == key1:
                    form1.fields[key].initial = getattr(sup, key)
            for key2 in form2.fields.keys():
                if key == key2:
                    form2.fields[key].initial = getattr(sup, key)
    return render(request, 'WISH/supplier_form.html',\
         {'form1': form1, 'form2': form2})

def par_form(request, pk):
    """function"""
    parss = get_object_or_404(PAR, pk=pk)
    products = parss.product
    for product in products:
        pro = Product.objects.get(id=product['Product'])
        amount = float(product['Quantity']) * int(pro.unit_cost)
        product['amount'] = amount
        product['pros'] = pro
        product['description'] = pro.description
        product['item_name'] = pro.item_name
        product['unit'] = pro.unit_measure
        product['from'] = pro.purchased_from
    if len(products) > 5:
        loop = len(products) / 5
        if len(products) % 5 != 0:
            loop = loop + 1
            remain = 5 - (len(products) % 5)
        return render(request, 'WISH/par_form.html', {'parss':parss,\
         'products': products, 'loop': range(loop), 'remain': range(remain)})
    else:
        loop = 1
        remain = 5 - len(products)
        return render(request, 'WISH/par_form.html', {'parss':parss, 'products': \
         products, 'remain': range(remain), 'loop': range(loop)})

def garv_form(request, pk):
    """function"""
    garvs = get_object_or_404(GARV, pk=pk)
    products = garvs.product_to_GARV
    for product in products:
        pro = Product.objects.get(id=product['Product'])
        product['pros'] = pro
    if len(products) > 3:
        loop = len(products) / 3
        if len(products) % 3 != 0:
            loop = loop + 1
            remain = 3 - (len(products) % 3)
        return render(request, 'WISH/garv_form.html', {'garvs':garvs, \
         'products': products, 'loop': range(loop), 'remain': range(remain)})
    else:
        loop = 1
        remain = 3 - len(products)
        return render(request, 'WISH/garv_form.html', {'garvs': garvs, \
            'products': products, 'remain': range(remain), 'loop': range(loop)})

def irr_form(request, pk):
    """function"""
    irs = get_object_or_404(IRR, pk=pk)
    products = irs.product
    total = 0
    for product in products:
        pro = Product.objects.get(id=product['Product'])
        amount = float(product['quantity_accepted']) * int(pro.unit_cost)
        product['amount'] = amount
        product['pros'] = pro
        total = total + amount
    if len(products) > 6:
        loop = len(products) / 6
        if len(products) % 6 != 0:
            loop = loop + 1
            remain = 6 - (len(products) % 6)
        return render(request, 'WISH/irr_form.html', \
            {'irs':irs, 'products': products, 'loop': range(loop), \
            'total': total, 'remain': range(remain)})
    else:
        loop = 1
        remain = 6 - len(products)
        return render(request, 'WISH/irr_form.html', {'irs':irs, \
            'products': products, 'total': total, 'remain': range(remain),\
            'loop': range(loop)})

def miv_form(request, pk):
    """function"""
    mivs = get_object_or_404(MIV, miv_no=pk)
    products = mivs.irr_no.product
    for product in products:
        pro = Product.objects.get(id=product['Product'])
        amount = float(product['quantity_accepted']) * int(pro.unit_cost)
        product['amount'] = amount
        product['pros'] = pro
    if len(products) > 6:
        loop = len(products) / 6
        if len(products) % 6 != 0:
            loop = loop + 1
            remain = 6 - (len(products) % 6)
        return render(request, 'WISH/miv_form.html', {'mivs':mivs, \
            'products': products, 'loop': range(loop), 'remain': range(remain)})
    else:
        loop = 1
        remain = 6 - len(products)
        return render(request, 'WISH/miv_form.html', {'mivs':mivs, \
            'products':products, 'remain': range(remain), 'loop': range(loop)})

def wrs_form(request, pk):
    """function"""
    wrss = get_object_or_404(IRR, wrs_number=pk)
    pros = wrss.product
    for pro in pros:
        pro['product'] = Product.objects.get(id=pro['Product'])
    if len(pros) > 3:
        loop = len(pros) / 3
        if len(pros) % 3 != 0:
            loop = loop + 1
            remain = 3 - (len(pros) % 3)
        return render(request, 'WISH/wrs_form.html', {'wrss':wrss, 'pros': pros, \
            'loop': range(loop), 'remain': range(remain)})
    else:
        loop = 1
        remain = 3 - len(pros)
        return render(request, 'WISH/wrs_form.html', {'wrss': wrss, \
            'pros': pros, 'remain': range(remain), 'loop': range(loop)})
