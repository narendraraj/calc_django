from django.shortcuts import render
from django.http import HttpResponse, request, Http404

# Create your views here.


def account_home_view(request):
    
    context = {

    }
    return render(request, "account/account_home.html", context)