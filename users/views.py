from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.


def login_view(request):
    return HttpResponse('<h1>Hello</h1>')


def change_info(request):
    return None
