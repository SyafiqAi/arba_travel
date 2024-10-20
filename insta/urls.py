from django.urls import path
from .views import CreatePostView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_post/", CreatePostView.as_view(), name="create_post"),
    path("update_post/<int:post_id>/", views.update_post, name="update_post"),
    path("post/<int:post_id>/", views.view, name="view")
]
