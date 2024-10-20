from django.urls import path
from .views import CreatePostView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_post/", CreatePostView.as_view(), name="create_post")
]
