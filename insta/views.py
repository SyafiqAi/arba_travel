from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView
from insta.models import Post
from django.urls import reverse, reverse_lazy
from .forms import PostForm, CommentForm
from django.contrib.auth.models import User
import datetime

def index(request):
    context = {"posts": Post.objects.all()}
    return render(request, "insta/index.html", context)

def view(request, post_id):
    post = Post.objects.get(id=post_id)
    comment_list = post.comment_set.order_by('-created_at')
    comment_list = list(map(lambda comment: {
        "text": comment.text,
        "user": User.objects.get(id=comment.user_id)
    }, comment_list))
    comment_form = CommentForm()
    context = {
        "request": request, 
        "post": post, 
        "poster": post.user,
        "comment_form": comment_form,
        "comment_list": comment_list
    }

    if request.method == 'POST':
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.created_at = datetime.datetime.now()
        comment.user_id = request.user.id
        comment.post_id = post_id
        comment.save()
        return HttpResponseRedirect(reverse('view', kwargs={'post_id': post_id}))
    
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
