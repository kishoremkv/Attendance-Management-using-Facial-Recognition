from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    # print("Cur request",request)
    return HttpResponse("Hello, world. You are at attendance.")
