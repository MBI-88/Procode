from django.shortcuts import render

# Create your views here.

def index(request:str) -> render:
    return render(request,'base.html')
