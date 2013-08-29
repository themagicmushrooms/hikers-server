from django.shortcuts import render


def home(request):
    response = render(request, "home.html")
    return response


def landing(request):
    response = render(request, "landing.html")
    return response
