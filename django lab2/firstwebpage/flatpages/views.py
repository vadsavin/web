from django.shortcuts import render
from django.shortcuts import render
from django import template
from django.http import HttpResponse

# Create your views here.
def home(request):
 return render(request, 'templates/static_handler.html')
def hello(request):
    return HttpResponse(u'Hello, world!')