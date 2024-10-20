from django.http import HttpResponse
from django.shortcuts import render

from insta.models import Post

def index(request):
    context = {"posts": Post.objects.all()}
    return render(request, "insta/index.html", context)

def create_post(request):
    return render(request, "insta/create_post.html")