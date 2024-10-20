from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView
from insta.models import Post, Comment
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
        "comment": comment,
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
        if 'comment' in request.POST:
            comment_id = request.POST.get('comment')
            if not comment_id:
                form = CommentForm(request.POST)
                comment = form.save(commit=False)
                comment.created_at = datetime.datetime.now()
                comment.user_id = request.user.id
                comment.post_id = post_id
                comment.save()
            else:
                comment = Comment.objects.get(id = comment_id)
                form = CommentForm(request.POST, instance=comment)
                form.save()
            context["comment_form"] = CommentForm()
        elif 'delete_comment' in request.POST:
            comment_id = request.POST.get('delete_comment')
            comment = Comment.objects.get(id = comment_id)
            comment.delete()
        elif 'edit_comment' in request.POST:
            comment_id = request.POST.get('edit_comment')
            comment = Comment.objects.get(id = comment_id)
            form = CommentForm(instance=comment)
            context['comment_form'] = form
            return render(request, "insta/view_post.html", context)
        elif 'delete_post' in request.POST:
            post_id = request.POST.get('delete_post')
            post = Post.objects.get(id = post_id)
            post.delete()
            return redirect('/')

        return redirect(request.META['HTTP_REFERER'])
    
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

def update_post(request, post_id):
    post = Post.objects.get(id = post_id)
    form = PostForm(instance=post)
    context = {
        "form": form,
        "post": post
    }

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            post.save()
            return redirect('/')
        else:
            return HttpResponse('fuck you')
        
    
    return render(request, "insta/update_post.html", context)