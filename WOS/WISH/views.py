from django.shortcuts import render
from .models import *

# Create your views here.
def wrs_form(request):
    return render(request, 'WISH/wrs_form.html', {})

def par_form(request):
    return render(request, 'WISH/par_form.html', {})
    
def cme_form(request):
    return render(request, 'WISH/cme_form.html', {})
