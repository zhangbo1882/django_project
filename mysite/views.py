from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

# Create your views here.
def home_main(request):
    html = render(request, 'index.html', "")
    return HttpResponse(html)
    
