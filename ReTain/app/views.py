from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
import sys
from django.http import HttpResponse
import base64

# Create your views here.
def index(request):
    if request.method == "POST":
        png_recovered = base64.decodestring((request.__dict__["_post"]["data"]))

    return render(request, "index.html")
