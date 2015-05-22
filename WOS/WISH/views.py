# Create your views here.
# pylint: disable=bare-except,invalid-name, too-many-branches


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
show_product = []

def log_in(request):
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
                        ['username1'], first_name=form1.data['first_name'],\
                        last_name=form1.data['last_name'], \
                        password=form1.data['password1'], email=None)

                        emp.user_id_id = user.id
                        emp.save()
                        msg = "You've successfully created an account."
                        form = forms.LoginForm()
                        form1 = forms.SignUpForm()
                        return render(request, 'WISH/login.html', \
                            {'form':form, 'form1': form1, 'msg': msg})
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
                    return redirect('WISH.views.index')
                    # Redirect to a success page.
                else:
                    form1 = forms.SignUpForm()
                    return render(request, 'WISH/login.html', \
                        {'error': 'Username and password does not match.',\
                         'form':form, 'form1': form1})
    else:
        form = forms.LoginForm()
        form1 = forms.SignUpForm()
        return render(request, 'WISH/login.html', \
            {'form': form, 'form1': form1})

@login_required
def log_out(request):
    logout(request)
    form = forms.LoginForm()
    form1 = forms.SignUpForm()
    return render(request, 'WISH/login.html', \
        {'form': form, 'form1': form1})

@login_required
def index(request):
    """function"""
    product = Product.objects.order_by('id')[:3]
    if len(product) == 0:
        product = None
    try:
        irr = IRR.objects.latest('wrs_number')
    except:
        irr = None
    try:
        par = PAR.objects.latest('par_no')
    except:
        par = None
    try:
        garv = GARV.objects.latest('garv_no')
    except:
        garv = None
    try:
        inv = InventoryStat.objects.latest('id')
    except:
        inv = None
    try:
        sup = Supplier.objects.latest('id')
    except:
        sup = None
    try:
        cc = CostCenter.objects.latest('id')
    except:
        cc = None
    return render(request, 'WISH/index.html', \
        {'product': product, 'irr': irr, \
        'par': par, 'garv': garv, 'inv': inv, \
        'sup': sup, 'cc': cc})

@login_required
def guest(request):
    """function"""
    return render(request, 'WISH/index.html', {})

@login_required
def aboutus(request):
    """function"""
    return render(request, 'WISH/AboutUs.html', {})

@login_required
def inv_stat_del(request, pk):
    """function"""

    inv_del = get_object_or_404(InventoryStat, pk=pk)
    inv_del.is_delete = True
    inv_del.save()
    msg = 'Inventory Station was deleted successfully.'
    try:
        return render(request, 'WISH/index.html', {'msg':msg})
    except:
        return render(request, 'WISH/index.html', {})

@login_required
def cost_center_del(request, pk):
    """function"""
    
    cos_del = get_object_or_404(CostCenter, pk=pk)
    cos_del.is_delete = True
    cos_del.save()
    msg = 'Cost center was deleted successfully.'
    try:
        return render(request, 'WISH/index.html', {'msg':msg})
    except:
        return render(request, 'WISH/index.html', {})

@login_required
def supplier_del(request, pk):
    """function"""

    sup_del = get_object_or_404(Supplier, pk=pk)
    sup_del.is_delete = True
    sup_del.save()
    msg = 'Supplier was deleted successfully.'
    try:
        return render(request, 'WISH/index.html', {'msg':msg})
    except:
        return render(request, 'WISH/index.html', {})

@login_required
def employee_del(request, pk):
    """function"""

    em_del = get_object_or_404(Employee, pk=pk)
    em_del.is_delete = True
    em_del.save()
    msg = 'Employee was deleted successfully.'
    try:
        return render(request, 'WISH/index.html', {'msg':msg})
    except:
        return render(request, 'WISH/index.html', {})

@login_required
def add_inv_stat(request):
    """function"""

    if request.method == "POST":
        form = forms.Statlib(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            msg = 'Inventory Station was added successfully.'
    else:
        form = forms.Statlib()
    try:
        form = forms.Statlib()
        return render(request, 'WISH/add_inv_stat.html', \
            {'form': form, 'msg':msg})
    except:
        return render(request, 'WISH/add_inv_stat.html', {'form': form})

@login_required
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
    else:
        form = forms.Suplib()
        form1 = forms.Suplib1()
        form2 = forms.Suplib2()
    try:
        return render(request, 'WISH/add_supplier.html', \
            {'form1': form1, 'form2': form2, 'msg':msg})
    except:
        return render(request, 'WISH/add_supplier.html', \
            {'form1': form1, 'form2': form2})

@login_required
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
            msg = 'Employee was added successfully.'
    else:
        form = forms.Emlib()
    try:
        form = forms.Emlib()
        return render(request, 'WISH/add_employee.html', {'form': form,\
         'msg':msg})
    except:
        return render(request, 'WISH/add_employee.html', {'form': form})

@login_required
def add_cost_center(request):
    """function"""

    if request.method == "POST":
        form = forms.CClib(request.POST)
        if form.is_valid():
            product = form.save(commit=False)

            product.save()
            msg = 'Cost center was added successfully.'
    else:
        form = forms.CClib()
    try:
        form = forms.CClib()
        return render(request, 'WISH/add_cost_center.html',\
         {'form': form, 'msg':msg})
    except:
        return render(request, 'WISH/add_cost_center.html', {'form': form})

@login_required
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

            #Message to be returned if adding of the new product entry.
            msg = 'Product (' + form1.data['item_name'] + ')\
             was added successfully.'

            #Displaying of blank forms
            form1 = forms.ProductForm1()
            form2 = forms.ProductForm2()
            form3 = forms.ProductForm3()
    else:
        #Displaying of blank forms
        form = forms.ProductForm()
        form1 = forms.ProductForm1()
        form2 = forms.ProductForm2()
        form3 = forms.ProductForm3()

    #Rendering of forms and/or messages
    try:
        return render(request, 'WISH/product_add.html', {'form3': form3,\
         'form1':form1, 'form2': form2, 'msg': msg})
    except:
        return render(request, 'WISH/product_add.html', {'form3': form3, \
            'form1':form1, 'form2': form2})

@login_required
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

            return redirect('WISH.views.product_to_irr',\
             pk=irr_entry.pk, inv=int(irr_entry.inv_station_no_id))
    else:
        prodlist = Product.objects.filter(is_irr=False)

        if len(prodlist) == 0:
            #If true return this exit message
            exit = 'No available products to be made with IRR record.'
        else:
            #else display blank forms.
            form1 = forms.IRRentryForm1(name=name)
            form2 = forms.IRRentryForm2(name=name)

    #Rendering of forms
    try:
        return render(request, 'WISH/irr_entry.html',\
         {'exit': exit})
    except:
        return render(request, 'WISH/irr_entry.html',\
         {'form1': form1, 'form2': form2})

@login_required
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
            #del show_product[k]['pros']
            prod_to_irr.remove(prod_to_irr[k])
            #pr.remove(show_product[k])

        #Non-empty forms are to be validated.
        elif form.is_valid() and iform.is_valid():

            #To check if the desired quantity of products
                #to be delivered are delivered already.
            if int(form.data['quantity_balance']) == 0:
                p = Product.objects.get(id=int(form.data['product']))
                p.balance = 0
                p.status = 'Complete'
                p.save()

            #To check if quantity accepted entered is 
                #less than the present stocked items.
            if Product.objects.get(id=int(form.data['product'])).quantity \
            < int(form.data['quantity_accepted']):
                error = 'Accepted quantity is greater than \
                the number of stocked items.'

            #To check if the delivering process of
                #the product is already completed.
            elif Product.objects.get(id=int\
                (form.data['product'])).status == 'Pending':
                error = 'Product -' + str(Product.objects.get(id=int\
                    (form.data['product'])).item_name) +\
                      '- is still pending.'

            else:
                #Storing of products for this specific IRR form.
                prod_to_irr.append({'Product': form.data['product'], \
                    'quantity_accepted': \
                int(form.data['quantity_accepted']), \
                'quantity_rejected':int(form.data['quantity_rejected']), \
                'quantity_balance': int(form.data['quantity_balance']), \
                'is_par':False, \
                'quantity_par': int(form.data['quantity_accepted'])})
                #show_product.append({'Product': form.data['product'], \
                #    'quantity_accepted': \
                #int(form.data['quantity_accepted']), \
                #'quantity_rejected':int(form.data['quantity_rejected']), \
                #'quantity_balance': int(form.data['quantity_balance']), \
                #'is_par':False, \
                #'quantity_par': int(form.data['quantity_accepted'])})
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

                irr.irr_headkey_id = pk

                for prod in prod_to_irr:
                    if 'pros' in prod:
                        del prod['pros']

                res = json.dumps(prod_to_irr)
                irr.product = res

                #To check if all entries for the IRR form is filled.
                if 'save' in request.POST:
                    msg = 'IRR record (IRR No. - ' + \
                        irr.irr_no + ') was successfully added.'
                    iform = forms.IRRentrycontForm(inv=inv)
                    del prod_to_irr[:]
                    del show_product[:]
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
        try:
            return render(request, 'WISH/product_to_irr.html', \
                {'exit': exit, 'remove_add': remove_add, 'msg': msg})
        except:
            return render(request, 'WISH/product_to_irr.html', \
                {'form': form, 'iform': iform, 'remove_add': \
                remove_add, 'error': error, 'product': prod_to_irr})
    except:
        try:
            return render(request, 'WISH/product_to_irr.html', \
                {'form': form, 'iform': iform, 'msg': msg, \
                'remove_add': remove_add, 'product': prod_to_irr})
        except:
            return render(request, 'WISH/product_to_irr.html', \
                {'form': form, 'iform': iform, 'remove_add': \
                remove_add, 'product': prod_to_irr})

@login_required
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

            prods = miv_entry.irr_no.product

            #Deducting the number of quantities to be pulled out by the user
            for prod in prods:
                p = Product.objects.get(id=(prod['Product']))
                p.quantity = int(p.quantity) - \
                int(prod['quantity_accepted'])
                p.amount = int(p.unit_cost) * int(p.quantity)
                p.average_amount = p.amount
                p.save()

            miv_entry.save()

            #Success message
            msg = 'MIV record (MIV No. - ' + \
                miv_entry.miv_no + ') was successfully added.'

            #Exit message
            exit = 'Exit'

            for prod in prods:
                p = Product.objects.get(id=(prod['Product']))
                p.quantity = int(p.quantity) - \
                int(prod['quantity_accepted'])
                if p.quantity < 0:
                    irr = IRR.objects.get(irr_no=pk)
                    irr.is_miv = True
                    irr.save()

    else:
        form = forms.MIVentryForm()

    #Rendering of forms and/or messages
    try:
        return render(request, 'WISH/miv_entry.html', \
            {'msg': msg, 'exit': exit})
    except:
        return render(request, 'WISH/miv_entry.html', {'form': form})

@login_required
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

@login_required
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

@login_required
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

@login_required
def product_to_garv(request, pk):
    """function"""

    prod_list = []
    error = ''
    msg = 3
    remove_add = 0
    products = PAR.objects.get(par_no=pk)
    for prod in products.product:
        if prod['is_garv'] == False:
            prod_list.append(int(prod['Product']))
    if request.method == "POST":
        form = forms.GARVentryForm(request.POST, pk=pk)
        iform = forms.ProducttoGARVform(request.POST, prodlist=prod_list)

        if form.is_valid() and iform.is_valid():
            garv = form.save(commit=False)

            garv_no = form.data['garv_no']

            for prod in products.product:
                if prod['Product'] == str(iform.data['product']):
                    prod['quantity_garv'] = int(prod['quantity_garv']) - \
                    int(iform.data['quantity'])
                    if int(prod['quantity_garv']) < 0:
                        error = 'Entered quantity is greater than \
                        accepted items.'
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
                prod_to_garv.append({'Product': iform.data['product'],\
                 'Quantity': \
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

                garv.confirmed_by = Employee.objects.get\
                (name=(str(request.user.first_name) + ' ' + \
                    str(request.user.last_name)))

                if len(prod_list) == 0:
                    products.is_garv = True
                    products.save()
                    garv.save()
                    del prod_to_garv[:]
                    exit = 'Exit'
                    return render(request, 'WISH/garv_entry.html', \
                        {'exit': exit, 'msg': \
                        'GARV Record (GARV No. - ' +\
                         str(garv_no) + ') is successfully added.'})

                if 'save' in request.POST:
                    msg = 0
                    garv.save()
                    del prod_to_par[:]
                    form = forms.GARVentryForm(pk=pk)
                    iform = forms.ProducttoGARVform(prodlist=prod_list)
                else:
                    msg = 1
                    iform = forms.ProducttoGARVform(prodlist=prod_list)
            else:
                msg = 2

    else:
        form = forms.GARVentryForm(pk=pk)
        iform = forms.ProducttoGARVform(prodlist=prod_list)

    if len(prod_list) == 1:
        remove_add = 1

    if int(msg) == 0:
        return render(request, 'WISH/garv_entry.html', \
            {'form': form, 'iform': iform, 'remove_add': \
            remove_add, 'msg': 'GARV Record (GARV No. - ' \
                + str(garv_no) + \
                ') is successfully added.'})
    elif int(msg) == 1:
        return render(request, 'WISH/garv_entry.html', \
            {'form': form, 'iform': iform, 'remove_add': \
            remove_add, 'msg': 'Item is successfully added.'})
    elif int(msg) == 2:
        return render(request, 'WISH/garv_entry.html', \
            {'form': form, 'iform': iform, 'remove_add': \
            remove_add, 'error': 'Entered product quantity \
            to be assigned to this employee is greater than\
             stocked items.'})
    else:
        return render(request, 'WISH/garv_entry.html', \
            {'form': form, 'iform': iform, 'remove_add': \
            remove_add})

@login_required
def par(request, inv):
    """function"""

    prod_list = []
    error = ''
    msg = 3
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
                if prod['Product'] == show_product[k]['Product']:
                    prod['quantity_par'] = show_product[k]['Quantity']
                    prod['is_par'] = False 
                    prod_list.append(int(prod['Product']))
            products.is_par = False
            products.save()
            show_product.remove(show_product[k])
            prod_to_par.remove(show_product[k])
            iform = forms.ProducttoPARForm(prodlist=prod_list)

        elif form.is_valid() and iform.is_valid():
            par_entry = form.save(commit=False)

            par_no = form.data['par_no']

            for prod in products.product:
                if prod['Product'] == str(iform.data['product']):
                    prod['quantity_par'] = int(prod['quantity_par'])\
                     - int(iform.data['quantity'])
                    if int(prod['quantity_par']) < 0:
                        error = 'Entered quantity is greater than \
                        stocked items.'
                    elif int(prod['quantity_par']) == 0:
                        prod['quantity_par'] = 0
                        prod['is_par'] = True
                        prod_list.remove(int(prod['Product']))
                        products.save()
                    else:
                        prod['quantity_par'] = prod['quantity_par']

            if error == '':
                par_entry.wo_number = IRR.objects.get(irr_no=inv)
                par_entry.par_date = time.strftime("%Y-%m-%d")
                prod_to_par.append({'Product': iform.data['product'],\
                                'Quantity': iform.data['quantity'], \
                                'quantity_garv': iform.data['quantity'],\
                                'is_garv': False})
                show_product.append({'Product': iform.data['product'],\
                                'Quantity': iform.data['quantity'], \
                                'quantity_garv': iform.data['quantity'],\
                                'is_garv': False})
                par_entry.amt_cost = 0
                for product in prod_to_par:
                    pro = Product.objects.get(id=product['Product'])
                    amount = float(product['Quantity']) * \
                    int(pro.unit_cost)
                    par_entry.amt_cost = par_entry.amt_cost + amount

                res = json.dumps(prod_to_par)
                par_entry.product = prod_to_par
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
                    exit = 'Exit'
                    return render(request, 'WISH/par_entry.html', \
                        {'exit': exit, 'msg': 'PAR Record (PAR No. - '\
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
                    for prod in show_product:
                        pro = Product.objects.get(id=int(prod['Product']))
                        prod['pros'] = pro
                iform = forms.ProducttoPARForm(prodlist=prod_list)
            else:
                msg = 2
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
            'msg': 'Item is successfully added.', 'product': show_product})
    elif int(msg) == 2:
        return render(request, 'WISH/par_entry.html', {'form': form,\
         'iform': iform, 'remove_add': remove_add, \
            'error': 'Entered product quantity to be assigned to this \
            employee is greater than stocked items.', 'product': show_product})
    else:
        return render(request, 'WISH/par_entry.html', {'form': form, \
            'iform': iform, 'remove_add': remove_add, 'product': show_product})


#def wrs_entry(request):
#    """function"""
#    
#        if 'q' in request.GET and request.GET['q']:
#            q = request.GET['q']
#            return redirect('WISH.views.wrs_form', pk=q)
#        return render(request, 'WISH/wrs_entry.html', {})
#    else:
#        form = forms.LoginForm(request.POST or None)
#        if form.is_valid():
#            user = authenticate(username=form.data['username'], \
#                password=form.data['password'])
#            if user is not None:
#                login(request, user)
#                return redirect('WISH.views.wrs_entry')
            # Redirect to a success page.
#            else:
#                return render(request, 'registration/login2.html', \
#                    {'error': 'Username and password does not match.',\
#                     'form':form})
#        else:
#            return render(request, 'registration/login2.html', {'form': form})
#        form = forms.LoginForm()"""

@login_required
def product_details(request, pk):
    """function"""

    prod = get_object_or_404(Product, pk=pk)
    return render(request, 'WISH/product_details.html', {'prod': prod})

@login_required
def inv_stat_details(request, pk):
    """function"""

    invs = get_object_or_404(InventoryStat, inv_station_no=pk)
    return render(request, 'WISH/inv_stat_details.html', {'invs': invs})

@login_required
def cost_center_details(request, pk):
    """function"""

    cc = get_object_or_404(CostCenter, pk=pk)
    return render(request, 'WISH/cost_center_details.html', {'cc': cc})

@login_required
def supplier_details(request, pk):
    """function"""

    sup = get_object_or_404(Supplier, supplier_number=pk)
    return render(request, 'WISH/supplier_details.html', {'sup': sup})

@login_required
def employee_details(request, dce):
    """function"""

    em = get_object_or_404(Employee, dce=dce)
    return render(request, 'WISH/employee_details.html', {'em': em})

@login_required
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
            if int(form2.data['quantity']) > 1:
                if form2.data['unit_measure'] == 'box':
                    product.unit_measure = str(product.unit_measure) + 'es'
                else:
                    product.unit_measure = str(product.unit_measure) + 's'
            product.amount = float(form2.data['unit_cost']) * \
            int(form2.data['quantity'])
            product.save()
            return redirect('WISH.views.index')
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
    return render(request, 'WISH/product_form.html', \
        {'form1': form1, 'form2': form2, 'form3': form3})

@login_required
def inv_stat_form(request, pk):
    """function"""

    inv = get_object_or_404(InventoryStat, pk=pk)
    form = forms.Statlib(request.POST or None, instance=inv)
    if form.is_valid():
        form.save()
        msg = 'Inventory Station was editted successfully.'
    try:
        form = forms.Statlib(request.POST or None, instance=inv)
        return render(request, 'WISH/inv_stat_form.html', \
            {'form': form, 'msg':msg})
    except:
        return render(request, 'WISH/inv_stat_form.html', {'form': form})

@login_required
def cost_center_form(request, pk):
    """function"""

    cc = get_object_or_404(CostCenter, pk=pk)
    form = forms.CClib(request.POST or None, instance=cc)
    if form.is_valid():
        form.save()
        msg = 'Cost center was editted successfully.'
    try:
        form = forms.CClib(request.POST or None, instance=cc)
        return render(request, 'WISH/cost_center_form.html',\
         {'form': form, 'msg':msg})
    except:
        return render(request, 'WISH/cost_center_form.html', {'form': form})

@login_required
def supplier_form(request, pk):
    """function"""

    sup = get_object_or_404(Supplier, supplier_number=pk)
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
            msg = 'Supplier information was editted successfully.'
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
    try:
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
        return render(request, 'WISH/supplier_form.html', \
            {'form1': form1, 'form2': form2, 'msg':msg})
    except:
        return render(request, 'WISH/supplier_form.html',\
         {'form1': form1, 'form2': form2})

@login_required
def employee_form(request, dce):
    """function"""

    em = get_object_or_404(Employee, dce=dce)
    form = forms.Employeelib(request.POST or None, instance=em)
    if form.is_valid():
        form.save()
        msg = 'Employee information was editted successfully.'
    try:
        form = forms.Employeelib(request.POST or None, instance=em)
        return render(request, 'WISH/employee_form.html', \
            {'form': form, 'msg':msg})
    except:
        return render(request, 'WISH/employee_form.html', {'form': form})

@login_required
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
        return render(request, 'WISH/par_form.html',\
         {'parss':parss, 'products': products, \
            'loop': range(loop), 'remain': range(remain)})
    else:
        remain = 5 - len(products)
        return render(request, 'WISH/par_form.html',\
         {'parss':parss, 'products': products, 'remain': range(remain)})

@login_required
def garv_form(request, pk):
    """function"""

    garvs = get_object_or_404(GARV, pk=pk)
    products = garvs.producttoGARV
    for product in products:
        pro = Product.objects.get(id=product['Product'])
        product['pros'] = pro
    if len(products) > 3:
        loop = len(products) / 3
        if len(products) % 3 != 0:
            loop = loop + 1
            remain = 3 - (len(products) % 3)
        return render(request, 'WISH/garv_form.html',\
         {'garvs':garvs, 'products': products, 'pro': pro,\
            'loop': range(loop), 'remain': range(remain)})
    else:
        loop = 1
        remain = 3 - len(products)
        return render(request, 'WISH/garv_form.html', \
            {'garvs': garvs, 'products': products, 'pro':pro,\
            'remain': range(remain), 'loop': range(loop)})

@login_required
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
            {'irs':irs, 'products': products, \
            'loop': range(loop), 'total': total, 'remain': range(remain)})
    else:
        loop = 1
        remain = 6 - len(products)
        return render(request, 'WISH/irr_form.html', \
            {'irs':irs, 'products': products, \
            'total': total, 'remain': range(remain),\
            'loop': range(loop)})

@login_required
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
        return render(request, 'WISH/miv_form.html', \
            {'mivs':mivs, 'products': products, \
            'loop': range(loop), 'remain': range(remain)})
    else:
        loop = 1
        remain = 6 - len(products)
        return render(request, 'WISH/miv_form.html', \
            {'mivs':mivs, 'products':products, 'remain': range(remain),\
            'loop': range(loop)})

@login_required
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
        return render(request, 'WISH/wrs_form.html', \
            {'wrss':wrss, 'pros': pros, \
            'loop': range(loop), 'remain': range(remain)})
    else:
        loop = 1
        remain = 3 - len(pros)
        return render(request, 'WISH/wrs_form.html', \
            {'wrss': wrss, 'pros': pros, 'remain': range(remain),\
            'loop': range(loop)})
