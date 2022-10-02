from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

# Create your views here.
def index(request):
    if request.method == "POST":
        image_url = request.POST["image"]
        
    return render(request, "index.html")
