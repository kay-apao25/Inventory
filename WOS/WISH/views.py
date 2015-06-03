# Create your views here.
# pylint: disable=bare-except,invalid-name, too-many-branches, unused-variable, too-many-statements, too-many-locals

"""views"""
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from WISH.models import Supplier, Product, PAR, GARV, CostCenter, \
        InventoryStat, Employee, IRR, MIV
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django_ajax.decorators import ajax
from django.db import IntegrityError
from WISH import forms
import time
import ast
import json

prod_to_par = []
prod_to_irr = []
prod_to_garv = []
prod_to_wrs = []
prods = []
query = 0

def log_in(request):
    """function"""
    if request.method == 'POST':
        if 'signup' in request.POST:
            form = forms.LoginForm()
            form1 = forms.SignUpForm(request.POST or None)
            form2 = forms.GuestForm()
            if form1.is_valid():
                dce = form1.data['dce']
                try:
                    emp = Employee.objects.get(dce=dce)
                except:
                    return render(request, 'WISH/login.html', {'form':form, \
                         'form1': form1, 'error1': "Employee does not exist.", 'form2':form2})
                try:
                    if emp.position == "Property Custodian":
                        user = User.objects.create_superuser(username=form1.data\
                            ['username1'], first_name=form1.data['first_name'],
                            last_name=form1.data['last_name'], password=\
                            form1.data['password1'], email=None)
                        emp.user_id_id = user.id
                        emp.save()
                    else:
                        user = User.objects.create_user(username=form1.data\
                            ['username1'], first_name=form1.data['first_name'],
                            last_name=form1.data['last_name'], password=\
                            form1.data['password1'], email=None)

                    form1 = forms.SignUpForm()
                    return render(request, 'WISH/login.html', {'form':form, \
                         'form1': form1, 'msg': "You've successfully created an account.", 'form2':form2})
                except:
                    return render(request, 'WISH/login.html', \
                        {'error1': 'Username already exists.',\
                         'form':form, 'form1': form1, 'form2':form2})

        elif 'login' in request.POST:
            form = forms.LoginForm(request.POST or None)
            form1 = forms.SignUpForm()
            form2 = forms.GuestForm()
            if form.is_valid():
                user = authenticate(username=form.data['username'], \
                    password=form.data['password'])
                if user is not None:
                    login(request, user)
                    form = forms.LoginForm()
                    return redirect('index')
                else:
                    return render(request, 'WISH/login.html', \
                        {'error': 'Username and password does not match.',\
                         'form':form, 'form1': form1, 'form2':form2})
        elif 'guest' in request.POST:
            form = forms.LoginForm()
            form1 = forms.SignUpForm()
            form2 = forms.GuestForm(request.POST or None)
            if form2.is_valid():
                if len(Employee.objects.filter(dce=int(form2.data['dce']))) != 0:
                    name = Employee.objects.get(dce=int(form2.data['dce'])).name
                    form2 = forms.GuestForm()
                    return redirect('guest', user=name)
                else:
                    return render(request, 'WISH/login.html', \
                        {'error2': 'Employee does not exist.',\
                         'form':form, 'form1': form1, 'form2':form2})
    else:
        form = forms.LoginForm()
        form1 = forms.SignUpForm()
        form2 = forms.GuestForm()
        return render(request, 'WISH/login.html', \
            {'form': form, 'form1': form1, 'form2':form2})

def log_out(request):
    """function"""
    logout(request)
    form = forms.LoginForm()
    form1 = forms.SignUpForm()
    form2 = forms.GuestForm()
    return render(request, 'WISH/login.html', {'form': form, 'form1': form1, 'form2':form2})

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

            sup.supplier_name = form.data['supplier_name']
            sup.save()
            return redirect('inv_stat')
    else:
        form = forms.Suplib()
        form1 = forms.Suplib1()
        form2 = forms.Suplib2()
    return render(request, 'WISH/add_supplier.html', \
        {'form1': form1, 'form2': form2})

def product_new(request):
    """function"""
    name = str(request.user.get_full_name())
    inv = Employee.objects.get(name=name).cost_center_no.inv_station_no

    if request.method == 'POST':
        #Forms containing the entries entered by the user
        form = forms.ProductForm(request.POST)
        form1 = forms.ProductForm1(request.POST)
        form2 = forms.ProductForm2(request.POST)
        form3 = forms.ProductForm3(request.POST)

        #Non-empty forms are to be validated.
        if form.is_valid() and form1.is_valid() \
        and form2.is_valid() and form3.is_valid():
            
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
                if key == 'purchased_from':
                    sup = form3.data['purchased_from']
                    sup = sup.split(', ')
                    product.purchased_from = Supplier.objects.filter(supplier_name=sup[1]).get(supplier_number=int(sup[0]))
                else:
                    setattr(product, key, form1.data[key])
                    setattr(product, key, form2.data[key])
                    setattr(product, key, form3.data[key])

            product.inv_station_no = inv
            if form2.data['expiry_date'] == '':
                product.expiry_date = None

            if int(form2.data['quantity']) > 1:
                if form2.data['unit_measure'] == 'box':
                    product.unit_measure = str(product.unit_measure) + 'es'
                else:
                    product.unit_measure = str(product.unit_measure) + 's'

            product.amount = float(form2.data['unit_cost']) * \
                float(form2.data['quantity'])
            product.save()

            #Displaying of blank forms
            form1 = forms.ProductForm1()
            form2 = forms.ProductForm2()
            form3 = forms.ProductForm3()

            return render(request, 'WISH/product_add.html', {'form3': form3,\
             'form1':form1, 'form2': form2, 'msg': 'Product -' + product.item_name \
             + '- (SLC No: ' + product.slc_number + ') was added successfully.'})
    else:
        #Displaying of blank forms
        form1 = forms.ProductForm1()
        form2 = forms.ProductForm2()
        form3 = forms.ProductForm3()

    #Rendering of forms and/or messages
    return render(request, 'WISH/product_add.html', {'form3': form3, \
            'form1':form1, 'form2': form2})

def irr_entry(request):
    """function"""
    name = str(request.user.get_full_name())
    inv = Employee.objects.get(name=name).cost_center_no.inv_station_no

    if request.method == "POST":
        #Forms containing the entries entered by the user
        form = forms.IRRentryForm(request.POST)
        form1 = forms.IRRentryForm1(request.POST)
        form2 = forms.IRRentryForm2(request.POST, name=name)

        #Non-empty forms are to be validated.
        if form.is_valid() and form1.is_valid() and form2.is_valid():
            irr_entry = form.save(commit=False)

            #Assignment of values in IRR header model
            for key in form.data.keys():
                key1 = key
                if key == 'dce_user' or key == 'inv_station_no'\
                 or key == 'dce_approved':
                    key = key + '_id'
                if key == 'supplier':
                    sup = form1.data['supplier']
                    sup = sup.split(', ')
                    irr_entry.supplier = Supplier.objects.filter(supplier_name=sup[1]).get(supplier_number=int(sup[0]))
                else:
                    setattr(irr_entry, key, form1.data[key1])
                    setattr(irr_entry, key, form2.data[key1])

            irr_entry.inv_station_no = inv
            irr_entry.dce_custodian = Employee.objects.get(name=name)

            try:
                irr_entry.save()
            except IntegrityError as e:
                return render(request, 'WISH/irr_entry.html', {"error": "Record already exists."\
                    , 'form1': form1, 'form2': form2})
            del prods[:]
            return redirect('new_irr_cont',\
             pk=irr_entry.pk, inv=int(irr_entry.inv_station_no_id), sup=Supplier.objects.get(supplier_number=int(sup[0])).id)
    else:
        prodlist = Product.objects.filter(inv_station_no=inv)
        form1 = forms.IRRentryForm1()
        form2 = forms.IRRentryForm2(name=name)

        if len(prodlist) == 0:
            #If true return this exit message
            return render(request, 'WISH/irr_entry.html',\
              {'exit': 'No available products to be made with IRR record.'})

    return render(request, 'WISH/irr_entry.html', {'form1': form1, 'form2': form2})


def miv_entry(request, pk):
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
                p = Product.objects.get(id=(prod['product']))
                p.quantity = int(p.quantity) - \
                int(prod['qty_a'])
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
            (name=(str(request.user.get_full_name())))

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
        remain = 4 - len(products)
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
        pro = Product.objects.get(id=product['product'])
        amount = float(product['qty_a']) * int(pro.unit_cost)
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
        pro = Product.objects.get(id=product['product'])
        amount = float(product['qty_a']) * int(pro.unit_cost)
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
        pro['prod'] = Product.objects.get(id=pro['product'])
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

def handson(request):
    prods = Product.objects.all()
    iform = forms.IRRentrycontForm()
    return render(request, 'WISH/handsontable.html', {'prods': prods, 'iform': iform})

@ajax
def list_view(request):
    c = request.POST.get('data')
    if 'delete' in request.POST:
        d = request.POST.get('data2')
        #return c, d
        del prods[int(c):(int(d)+1)]
    else:
        del prod_to_irr[:]
        for c in json.loads(c):
            prod_to_irr.append(c)

def product_to_irr(request, pk, inv, sup):
    """function"""
    if len(prods) != 0:
        prodlist = Product.objects.filter(inv_station_no=inv).filter(\
                purchased_from=sup).filter(quantity__gt=0).exclude(\
                id__in=[p.id for p in prods])
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        prodlist = Product.objects.filter(inv_station_no=inv).filter(\
            purchased_from=sup).filter(quantity__gt=0).\
            filter(slc_number__contains=q).exclude(\
            id__in=[p.id for p in prods])
        pform = forms.ProductCheckForm(plist=prodlist)
        iform = forms.IRRentrycontForm()
        return render(request, 'WISH/product_to_irr.html', \
        {'iform': iform,  'pk': pk,'prods': prods, 'q': 1,\
        'pform': pform, 'inv': inv, 'sup': sup, 'prodlist': prodlist})
    elif 'add' in request.GET:
        q = request.GET.getlist('product')
        for q in q:
            prods.append(Product.objects.get(id=q))
        iform = forms.IRRentrycontForm()
        return render(request, 'WISH/product_to_irr.html', \
            {'iform': iform, 'pk': pk, 'prods': prods, \
            'inv': inv, 'sup': sup})
    elif 'save' in request.POST:
        iform = forms.IRRentrycontForm(request.POST)
        if iform.is_valid():
            for p in prod_to_irr:
                if 'qty_a' and 'qty_b' and 'qty_r' in p:
                    if Product.objects.get(id=p['product']).quantity < int(p['qty_a']):
                        return render(request, 'WISH/product_to_irr.html', \
                        {'iform': iform, 'error': 'Accepted quantity is greater than ' + \
                        'the number of stocked items.', 'pk': pk, 'inv':inv, 'sup':sup})
                else:
                    return render(request, 'WISH/product_to_irr.html', \
                        {'iform': iform, 'error': 'No entry for quantity accepted, ' +
                        'rejected and balance', 'pk': pk, 'inv':inv, 'sup':sup, 'prods': prods})
                p['is_par'] = False
                p['quantity_par'] = p['qty_a']
                p = Product.objects.get(id=p['product'])
                p.is_irr = True
                p.save()

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
            irr.cost_center_no = Employee.objects.get(name=str(\
                request.user.get_full_name())).cost_center_no

            #Generation of WRS number
            if len(IRR.objects.all()) != 0:
                no = int((IRR.objects.latest\
                    ('wrs_number')).wrs_number) + 1
                irr.wrs_number = str(no)
            else:
                irr.wrs_number = str(irr.irr_headkey.\
                    inv_station_no.id) + '000000'

            irr.product = json.dumps(prod_to_irr)
            del prod_to_irr[:]
            del prods[:]
            irr.save()
            return render(request, 'WISH/product_to_irr.html', \
            {'msg': 'IRR record (IRR No. - '+ irr.irr_no + \
            ') was successfully added.'})
        else:
            return redirect('index')
    elif 'cancel' in request.POST:
        del prod_to_irr[:]
        del prods[:]
        return render(request, 'WISH/product_to_irr.html', \
            {'msg': 'Making of IRR Record was cancelled.'})
    else:
        iform = forms.IRRentrycontForm()

    return render(request, 'WISH/product_to_irr.html', \
        {'iform': iform, 'pk': pk,'prods': prods,\
        'inv': inv, 'sup': sup})

def par(request, inv):
    """function"""
    name = str(request.user.get_full_name())
    prod_list = []
    msg = 2
    remove_add = 0
    products = IRR.objects.get(irr_no=inv)
    for prod in products.product:
        if prod['is_par'] == False:
            prod_list.append(int(prod['product']))
    if request.method == "POST":
        form = forms.PARForm(request.POST, name=name)
        iform = forms.ProducttoPARForm(request.POST, prodlist=prod_list)

        if 'delete' in request.POST:
            k = int(request.POST['delete'])
            for prod in products.product:
                if prod['product'] == prod_to_par[k]['Product']:
                    prod['quantity_par'] = prod_to_par[k]['Quantity']
                    prod['is_par'] = False
                    prod_list.append(int(prod['product']))
            products.is_par = False
            products.save()
            prod_to_par.remove(prod_to_par[k])
            iform = forms.ProducttoPARForm(prodlist=prod_list)

        elif form.is_valid() and iform.is_valid():
            par_entry = form.save(commit=False)

            par_no = form.data['par_no']

            for prod in products.product:
                if prod['product'] == str(iform.data['product']):
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
                        prod_list.remove(int(prod['product']))
                        products.save()
                    else:
                        prod['quantity_par'] = prod['quantity_par']

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
                if 'pros' in product:
                    del product['pros']

            par_entry.product = json.dumps(prod_to_par)
            par_entry.inv_stat_no_id = IRR.objects.get(irr_no=inv).\
            irr_headkey.inv_station_no.id

            par_entry.issued_by = Employee.objects.get\
            (name=(str(request.user.get_full_name())))

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
                form = forms.PARForm(name=name)
            else:
                msg = 1
                products.save()
                iform = forms.ProducttoPARForm(prodlist=prod_list)
                for prod in prod_to_par:
                    pro = Product.objects.get(id=int(prod['Product']))
                    prod['pros'] = pro
            iform = forms.ProducttoPARForm(prodlist=prod_list)

    else:
        form = forms.PARForm(name=name)
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
