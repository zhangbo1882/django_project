from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User

# Create your views here.
def home_main(request):
    if request.user.is_authenticated():
        html = render(request, 'index.html', {'logged' : True})
    else:
        html = render(request, 'index.html', {'logged' : False})
    return HttpResponse(html)
    
