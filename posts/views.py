from django.shortcuts import HttpResponse
import datetime
# Create your views here.

def main(request):
    return HttpResponse('Hello! its my first view!')

def hello(request):
    return HttpResponse('Hello! its my project')


def now_date(request):
    return HttpResponse(f'{datetime.datetime.now()}')


def goodby(request):
    return HttpResponse("Goodby user!")