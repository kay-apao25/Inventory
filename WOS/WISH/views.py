from django.shortcuts import render

# Create your views here.
def wrs_form(request):
    return render(request, 'WISH/wrs_form.html', {})