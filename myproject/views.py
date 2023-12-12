from django.shortcuts import render
from django.http import HttpResponse


# def hello_world(request):
#     return HttpResponse("Hello, World!")

def hello_world(request):
    return render(request, 'hello.html')

def main_page(request):
    return render(request, 'main.html')

def start_page(request):
    return render(request, 'start.html')
