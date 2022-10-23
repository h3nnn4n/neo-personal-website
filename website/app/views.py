from django.http import HttpResponse
from django.shortcuts import render  # noqa


def index(request):
    return HttpResponse("oi")
