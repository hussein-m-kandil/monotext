from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path("post/add/", views.PostView.as_view(), name="post_create"),
    path("comment/<int:post_pk>/add/",
         views.CommentView.as_view(), name="comment_create"),
    path("post/<int:post_pk>/comments/",
         views.PostCommentsView.as_view(), name="post_comments"),
]
