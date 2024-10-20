from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, "insta/index.html")

def create_post(request):
    return render(request, "insta/create_post.html")