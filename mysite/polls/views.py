from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def poll_main(request):
    html = "<html> <body>Hello World </body></html>"
    return HttpResponse(html)
