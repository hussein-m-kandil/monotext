from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path("profile/<username>", views.ProfileView.as_view(), name="profile"),
    path("post/add/", views.PostView.as_view(), name="post_create"),
    path("profile/<username>/post/<int:post_pk>/",
         views.PostView.as_view(), name="post_detail"),
    path("comment/<int:post_pk>/add/",
         views.CommentView.as_view(), name="comment_create"),
    path("post/<int:post_pk>/comments/",
         views.PostCommentsView.as_view(), name="post_comments"),
]
