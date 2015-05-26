from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy
from . import models
from . import forms

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
        return models.PAR.objects.filter(issued_by=(models.Employee.objects.get(\
        name=str(self.request.user.first_name) + ' ' + str(self.request.user.\
        last_name)))).filter(is_garv=False)

class IRRRep(ListView):
    context_object_name='irr_list' 
    template_name = 'WISH/irr_reports.html'

    def get_queryset(self):
        return models.IRR.objects.filter(irr_headkey__in=[i.id for i in (\
        models.IRRHeader.objects.filter(dce_custodian=(models.Employee.objects.get(\
        name=str(self.request.user.first_name) + ' ' + str(self.request.user.last_name\
        )))))])

class MIVRep(ListView):
    context_object_name='miv_list' 
    template_name = 'WISH/miv_reports.html'

    def get_queryset(self):
        return models.MIV.objects.filter(irr_no=models.IRR.objects.filter(\
        irr_headkey__in=[i.id for i in (models.IRRHeader.objects.filter(\
        dce_custodian=(models.Employee.objects.get(name=str(self.request.user.\
        first_name) + ' ' + str(self.request.user.last_name)))))]))

class WRSRep(ListView):
    context_object_name='wrs_list' 
    template_name = 'WISH/wrs_reports.html'

    def get_queryset(self):
        return models.IRR.objects.filter(irr_headkey__in=[i.id for i in (\
        models.IRRHeader.objects.filter(dce_custodian=(\
        models.Employee.objects.get(name=str(self.request.user.\
        first_name) + ' ' + str(self.request.user.last_name)))))])

class PARRep(ListView):
    context_object_name='par_list' 
    template_name = 'WISH/par_reports.html'

    def get_queryset(self):
        return models.PAR.objects.filter(issued_by=(models.Employee.objects.get(\
        name=str(self.request.user.first_name) + ' ' + str(self.request.user.\
        last_name))))

class GARVRep(ListView):
    context_object_name='garv_list' 
    template_name = 'WISH/garv_reports.html'

    def get_queryset(self):
        return models.GARV.objects.filter(confirmed_by=(models.Employee.objects.get(\
        name=str(self.request.user.first_name) + ' ' + str(self.request.user.\
        last_name))))

class ProdRep(ListView):
    context_object_name='product_list' 
    template_name = 'WISH/product_reports.html'

    def get_queryset(self):
        return models.Product.objects.filter(inv_station_no__in=[i.inv_station_no \
        for i in (models.InventoryStat.objects.filter(cost_center_no=(\
        models.Employee.objects.get(name=str(self.request.user.first_name) \
        + ' ' + str(self.request.user.last_name)).cost_center_no)))])

class InvStatRep(ListView):
    context_object_name='inv_list' 
    template_name = 'WISH/inv_stat.html'

    def get_queryset(self):
        return models.InventoryStat.objects.filter(is_delete=False).filter(\
        cost_center_no_id=(models.Employee.objects.get(name=str(self.\
        request.user.first_name) + ' ' + str(self.request.user.last_name\
        )).cost_center_no_id))

class CCRep(ListView):
    context_object_name='cc_list' 
    template_name = 'WISH/cost_center.html'

    def get_queryset(self):
        return models.CostCenter.objects.filter(is_delete=False)

class SupRep(ListView):
    context_object_name='sup_list' 
    template_name = 'WISH/supplier.html'

    def get_queryset(self):
        return models.Supplier.objects.filter(is_delete=False)

class EmpRep(ListView):
    context_object_name='em_list' 
    template_name = 'WISH/employee.html'

    def get_queryset(self):
        return models.Employee.objects.filter(is_delete=False).\
        filter(cost_center_no_id=(models.Employee.objects.get(\
        name=str(self.request.user.first_name) + ' ' + str(self.\
        request.user.last_name)).cost_center_no_id))

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

