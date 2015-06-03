from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from WISH.models import Supplier, CostCenter, InventoryStat, Employee, MIV, GARV, IRR, PAR, Product
from django.shortcuts import get_object_or_404, redirect, render
from django.core.urlresolvers import reverse_lazy
from . import models
from . import forms
import datetime

class ParF(ListView):
    context_object_name='irr_list'
    template_name = 'WISH/par_f.html'

    def get_queryset(self):
        return models.IRR.objects.filter(irr_headkey__in=[i.id for i in (\
        models.IRRHeader.objects.filter(dce_custodian=(models.Employee.objects.get(\
        name=str(self.request.user.first_name) + ' ' + str(self.request.user.last_name\
        )))))]).filter(is_par=False)

class MivF(ListView):
    context_object_name='irr_list'
    template_name = 'WISH/miv_entry_f.html'

    def get_queryset(self):
        return models.IRR.objects.filter(irr_headkey__in=[i.id for i in (\
        models.IRRHeader.objects.filter(dce_custodian=(models.Employee.objects.\
        get(name=str(self.request.user.first_name) + ' ' + str(self.request.user.\
        last_name)))))]).filter(is_miv=False)

class GarvF(ListView):
    context_object_name='par_list'
    template_name = 'WISH/garv_entry_f.html'

    def get_queryset(self):
        return models.PAR.objects.filter(is_garv=False)

class IRRRep(ListView):
    context_object_name='irr_list'
    template_name = 'WISH/irr_reports.html'


    def get_queryset(self):
        if 'q' in self.request.GET and self.request.GET['q']:
            q = self.request.GET['q']
            return models.IRR.objects.filter(irr_no__icontains=q)
        else:
            today = datetime.datetime.now()
            this_year = today.year
            this_month = today.month


            return models.IRR.objects.filter(irr_headkey__in=[i.id for i in (\
            models.IRRHeader.objects.filter(dce_custodian=(models.Employee.objects.get(\
            name=str(self.request.user.first_name) + ' ' + str(self.request.user.last_name\
            )))))]).filter(date_recv__year=str(this_year), date_recv__month=str(this_month))


    def get_context_data(self, **kwargs):
        if 'q' in self.request.GET and self.request.GET['q']:
            context = super(IRRRep, self).get_context_data(**kwargs)
            q = self.request.GET['q']
            if len(models.IRR.objects.filter(irr_no__icontains=q)):
                context['msg'] = 'Results Found:'
            else:
                context['error'] = 'No Results Found'
            return context

        else:
            context = super(IRRRep, self).get_context_data(**kwargs)
            return context

class MIVRep(ListView):
    context_object_name='miv_list'
    template_name = 'WISH/miv_reports.html'

    def get_queryset(self):

        if 'q' in self.request.GET and self.request.GET['q']:
            q = self.request.GET['q']
            return models.MIV.objects.filter(miv_no__icontains=q)
        else:
            today = datetime.datetime.now()
            this_year = today.year
            this_month = today.month

            return models.MIV.objects.filter(irr_no=models.IRR.objects.filter(\
            irr_headkey__in=[i.id for i in (models.IRRHeader.objects.filter(\
            dce_custodian=(models.Employee.objects.get(name=str(self.request.user.\
            first_name) + ' ' + str(self.request.user.last_name)))))]))\
            .filter(date_issued__year=str(this_year), \
            date_issued__month=str(this_month))

    def get_context_data(self, **kwargs):
        if 'q' in self.request.GET and self.request.GET['q']:
            context = super(MIVRep, self).get_context_data(**kwargs)
            q = self.request.GET['q']
            if len(models.MIV.objects.filter(miv_no__icontains=q)):
                context['msg'] = 'Results Found:'
            else:
                context['error'] = 'No Results Found'
            return context

        else:
            context = super(MIVRep, self).get_context_data(**kwargs)
            return context

class WRSRep(ListView):
    context_object_name='wrs_list'
    template_name = 'WISH/wrs_reports.html'

    def get_queryset(self):

        if 'q' in self.request.GET and self.request.GET['q']:
            q = self.request.GET['q']
            return models.IRR.objects.filter(wrs_number__icontains=q)
        else:
            today = datetime.datetime.now()
            this_year = today.year
            this_month = today.month

            return models.IRR.objects.filter(irr_headkey__in=[i.id for i in (\
            models.IRRHeader.objects.filter(dce_custodian=(\
            models.Employee.objects.get(name=str(self.request.user.\
            first_name) + ' ' + str(self.request.user.last_name)))))])\
            .filter(date_recv__year=str(this_year), date_recv__month=str(this_month))

    def get_context_data(self, **kwargs):
        if 'q' in self.request.GET and self.request.GET['q']:
            context = super(WRSRep, self).get_context_data(**kwargs)
            q = self.request.GET['q']
            if len(models.IRR.objects.filter(irr_no__icontains=q)):
                context['msg'] = 'Results Found:'
            else:
                context['error'] = 'No Results Found'
            return context

        else:
            context = super(WRSRep, self).get_context_data(**kwargs)
            return context


class WRSRep1(ListView):
    context_object_name='wrs_list'
    template_name = 'WISH/wrs_reports1.html'
    extra_context={'user': 'user'}

    def get_queryset(self):
        return models.IRR.objects.filter(irr_headkey__in=[i.id for i in (\
        models.IRRHeader.objects.filter(dce_user=(\
        models.Employee.objects.get(name=str(self.kwargs['user'])))))])

class PARRep(ListView):
    context_object_name='par_list'
    template_name = 'WISH/par_reports.html'

    def get_queryset(self):

        if 'q' in self.request.GET and self.request.GET['q']:
            q = self.request.GET['q']
            return models.PAR.objects.filter(par_no__icontains=q)
        else:
            today = datetime.datetime.now()
            this_year = today.year
            this_month = today.month

            return models.PAR.objects.filter(issued_by=(models.Employee.objects.get(\
            name=str(self.request.user.first_name) + ' ' + str(self.request.user.\
            last_name)))).filter(par_date__year=str(this_year), \
            par_date__month=str(this_month))

    def get_context_data(self, **kwargs):
        if 'q' in self.request.GET and self.request.GET['q']:
            context = super(PARRep, self).get_context_data(**kwargs)
            q = self.request.GET['q']
            if len(models.PAR.objects.filter(par_no__icontains=q)):
                context['msg'] = 'Results Found:'
            else:
                context['error'] = 'No Results Found'
            return context

        else:
            context = super(PARRep, self).get_context_data(**kwargs)
            return context

class GARVRep(ListView):
    context_object_name='garv_list'
    template_name = 'WISH/garv_reports.html'

    def get_queryset(self):
        if 'q' in self.request.GET and self.request.GET['q']:
            q = self.request.GET['q']
            return models.GARV.objects.filter(garv_no__icontains=q)
        else:
            today = datetime.datetime.now()
            this_year = today.year
            this_month = today.month

            return models.GARV.objects.filter(confirmed_by=(models.Employee.objects.get(\
            name=str(self.request.user.first_name) + ' ' + str(self.request.user.\
            last_name)))).filter(garv_date__year=str(this_year), \
            garv_date__month=str(this_month))

    def get_context_data(self, **kwargs):
        if 'q' in self.request.GET and self.request.GET['q']:
            context = super(GARVRep, self).get_context_data(**kwargs)
            q = self.request.GET['q']
            if len(models.GARV.objects.filter(garv_no__icontains=q)):
                context['msg'] = 'Results Found:'
            else:
                context['error'] = 'No Results Found'
            return context

        else:
            context = super(GARVRep, self).get_context_data(**kwargs)
            return context

class GARVRep1(ListView):
    context_object_name='garv_list'
    template_name = 'WISH/garv_reports1.html'

    def get_queryset(self):
        return models.GARV.objects.filter(dce=(models.Employee.objects.get(\
        name=str(self.kwargs['user'])).dce))

class ProdRep(ListView):
    context_object_name='product_list'
    template_name = 'WISH/product_reports.html'

    def get_queryset(self):
        return models.Product.objects.filter(inv_station_no=(models.Employee.objects.get(name=str(self.request.user.get_full_name())).cost_center_no.inv_station_no))

class InvStatRep(ListView):
    context_object_name='inv_list'
    template_name = 'WISH/inv_stat.html'

    def get_queryset(self):
        if 'q' in self.request.GET and self.request.GET['q']:
            q = self.request.GET['q']
            return models.InventoryStat.objects.filter(inv_station_no__icontains=q)
        else:
            return models.InventoryStat.objects.filter(is_delete=False).order_by('-id')[:1]

    def get_context_data(self, **kwargs):
        if 'q' in self.request.GET and self.request.GET['q']:
            context = super(InvStatRep, self).get_context_data(**kwargs)
            q = self.request.GET['q']
            if len(models.InventoryStat.objects.filter(inv_station_no__icontains=q)):
                context['msg'] = 'Results Found:'
            else:
                context['error'] = 'No Results Found'
            return context

        else:
            context = super(InvStatRep, self).get_context_data(**kwargs)
            return context

class CCRep(ListView):
    context_object_name='cc_list'
    template_name = 'WISH/cost_center.html'

    def get_queryset(self):
        if 'q' in self.request.GET and self.request.GET['q']:
            q = self.request.GET['q']
            return models.CostCenter.objects.filter(cost_center_name__icontains=q)
        else:
            return models.CostCenter.objects.filter(is_delete=False).order_by('-id')[:1]

    def get_context_data(self, **kwargs):
        if 'q' in self.request.GET and self.request.GET['q']:
            context = super(CCRep, self).get_context_data(**kwargs)
            q = self.request.GET['q']
            if len(models.CostCenter.objects.filter(cost_center_name__icontains=q)):
                context['msg'] = 'Results Found:'
            else:
                context['error'] = 'No Results Found'
            return context

        else:
            context = super(CCRep, self).get_context_data(**kwargs)
            return context

class SupRep(ListView):
    context_object_name='sup_list'
    template_name = 'WISH/supplier.html'

    def get_queryset(self):
        return models.Supplier.objects.filter(is_delete=False)

class EmpRep(ListView):
    context_object_name='em_list'
    template_name = 'WISH/employee.html'

    def get_queryset(self):
        if 'q' in self.request.GET and self.request.GET['q']:
            q = self.request.GET['q']
            return models.Employee.objects.filter(dce__icontains=q)
        else:
            return models.Employee.objects.filter(is_delete=False).\
            filter(cost_center_no_id=(models.Employee.objects.get(\
            name=str(self.request.user.first_name) + ' ' + str(self.\
            request.user.last_name)).cost_center_no_id)).order_by('-dce')[:1]

    def get_context_data(self, **kwargs):
        if 'q' in self.request.GET and self.request.GET['q']:
            context = super(EmpRep, self).get_context_data(**kwargs)
            q = self.request.GET['q']
            if len(models.Employee.objects.filter(dce__icontains=q)):
                context['msg'] = 'Results Found:'
            else:
                context['error'] = 'No Results Found'
            return context

        else:
            context = super(EmpRep, self).get_context_data(**kwargs)
            return context

class InvStatEntry(UpdateView):
    model = models.InventoryStat
    form_class = forms.Statlib1
    success_url = reverse_lazy('inv_stat')

class CostCenEntry(UpdateView):
    model = models.CostCenter
    form_class = forms.CClib
    success_url = reverse_lazy('cost_center')

class EmpEntry(UpdateView):
    model = models.Employee
    form_class = forms.Employeelib
    success_url = reverse_lazy('employee')

class ProdDetails(DetailView):
    model = models.Product
    context_object_name = 'prod'

class InvStatDetails(DetailView):
    model = models.InventoryStat
    context_object_name = 'invs'

class CCDetails(DetailView):
    model = models.CostCenter
    context_object_name = 'cc'

class SupDetails(DetailView):
    model = models.Supplier
    context_object_name = 'sup'

class EmpDetails(DetailView):
    model = models.Employee
    context_object_name = 'em'

class AddCC(CreateView):
    model = models.CostCenter
    form_class = forms.CClib
    template_name='WISH/add_cost_center.html'
    success_url = reverse_lazy('cost_center')

class AddInvStat(CreateView):
    model = models.InventoryStat
    form_class = forms.Statlib
    template_name='WISH/add_inv_stat.html'
    success_url = reverse_lazy('inv_stat')

class AddEmp(CreateView):
    model = models.Employee
    form_class = forms.Emlib
    template_name='WISH/add_employee.html'
    success_url = reverse_lazy('employee')

class InvStatRes(ListView):
    context_object_name='inv_list_res'
    template_name = 'WISH/inv_stat_res.html'

    def get_queryset(self):
        return models.InventoryStat.objects.filter(is_delete=True)

class CCRes(ListView):
    context_object_name='cc_list'
    template_name = 'WISH/cost_center_res.html'

    def get_queryset(self):
        return models.CostCenter.objects.filter(is_delete=True)

class SupRes(ListView):
    context_object_name='sup_list'
    template_name = 'WISH/supplier_res.html'

    def get_queryset(self):
        return models.Supplier.objects.filter(is_delete=True)

class EmpRes(ListView):
    context_object_name='em_list'
    template_name = 'WISH/employee_res.html'

    def get_queryset(self):
        return models.Employee.objects.filter(is_delete=True)

class InvStatDetailsRes(DetailView):
    model = models.InventoryStat
    context_object_name = 'invs'
    template_name = 'WISH/inv_stat_details_res.html'

class CCDetailsRes(DetailView):
    model = models.CostCenter
    context_object_name = 'cc'
    template_name = 'WISH/costcenter_detail_res.html'

class SupDetailsRes(DetailView):
    model = models.Supplier
    context_object_name = 'sup'
    template_name = 'WISH/supplier_detail_res.html'

class EmpDetailsRes(DetailView):
    model = models.Employee
    context_object_name = 'em'
    template_name = 'WISH/employee_detail_res.html'

""" Non-classes """

def inv_stat_del(request, pk):
    """function"""
    inv_del = get_object_or_404(InventoryStat, pk=pk)
    inv_del.is_delete = True
    inv_del.save()
    return redirect('inv_stat')

def cost_center_del(request, pk):
    """function"""
    cos_del = get_object_or_404(CostCenter, pk=pk)
    cos_del.is_delete = True
    cos_del.save()
    return redirect('cost_center')

def supplier_del(request, pk):
    """function"""
    sup_del = get_object_or_404(Supplier, pk=pk)
    sup_del.is_delete = True
    sup_del.save()
    return redirect('supplier')

def employee_del(request, pk):
    """function"""
    em_del = get_object_or_404(Employee, pk=pk)
    em_del.is_delete = True
    em_del.save()
    return redirect('employee')

def inv_stat_res(request, pk):
    """function"""
    inv_del = get_object_or_404(InventoryStat, pk=pk)
    inv_del.is_delete = False
    inv_del.save()
    return redirect('inv_stat')

def cost_center_res(request, pk):
    """function"""
    cc_del = get_object_or_404(CostCenter, pk=pk)
    cc_del.is_delete = False
    cc_del.save()
    return redirect('cost_center')

def supplier_res(request, pk):
    """function"""
    sup_del = get_object_or_404(Supplier, pk=pk)
    sup_del.is_delete = False
    sup_del.save()
    return redirect('supplier')

def employee_res(request, pk):
    """function"""
    em_del = get_object_or_404(Employee, pk=pk)
    em_del.is_delete = False
    em_del.save()
    return redirect('employee')

def index(request):
    """function"""
    try:
        product = Product.objects.order_by('id')[:4]
    except:
        product = []
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
        miv = MIV.objects.latest('miv_no')
    except:
        miv = None
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
    return render(request, 'WISH/index.html', {'product': product, 'irr': irr, \
    'par': par, 'garv': garv, 'miv': miv, 'inv': inv, 'sup': sup, 'cc': cc})

def aboutus(request):
    """function"""
    return render(request, 'WISH/AboutUs.html', {})
