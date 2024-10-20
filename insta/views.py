from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView
from insta.models import Post
from django.urls import reverse_lazy
from .forms import PostForm
from django.contrib.auth.models import User

def index(request):
    context = {"posts": Post.objects.all()}
    return render(request, "insta/index.html", context)

def view(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {"request": request, "post": post, "poster": post.user}
    return render(request, "insta/view_post.html", context)

def create_post(request):
    return render(request, "insta/create_post.html")

class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "insta/create_post.html"
    success_url = reverse_lazy("index")
    def form_valid(self, form):
        post = form.save(commit=False)
        post.user_id = self.request.user.id
        post.save()
        return HttpResponseRedirect("/")
