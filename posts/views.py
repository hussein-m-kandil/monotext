from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.serializers import serialize
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import PostModelForm, CommentModelForm
from .models import Post, Comment, Like

# Create your views here.


class IndexView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = "posts/index.html"
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_form"] = PostModelForm()
        context["comment_form"] = CommentModelForm()
        return context


class ProfileView(LoginRequiredMixin, generic.View):
    def get(self, request, username):
        post_list = (
            Post.objects
            .filter(owner=User.objects.get(username=username))
            .select_related().order_by("-created_at")
        )
        # Paginator
        paginator = Paginator(post_list, 3, allow_empty_first_page=True)
        # Page number
        page_number = request.GET.get("page", False)
        if (page_number):
            page_obj = paginator.get_page(page_number)
        else:
            page_obj = paginator.get_page(1)
        return render(
            request=request,
            template_name="posts/profile.html",
            context={
                "owner": self.request.user,
                "post_list": page_obj.object_list,
                "object_list": post_list,
                "is_paginated": True,
                "page_obj": page_obj,
                "paginator": paginator,
            }
        )


class PostView(LoginRequiredMixin, generic.View):
    def get(self, request, username, post_pk):
        return render(
            request=request,
            template_name="posts/post_detail.html",
            context={
                "post": get_object_or_404(Post, pk=post_pk),
            },
        )

    def post(self, request):
        post_form = PostModelForm(data=request.POST)
        if not post_form.is_valid():
            return JsonResponse(post_form.errors)
        # Add the post's owner before saving it
        post = post_form.save(commit=False)
        post.owner = self.request.user
        post.save()
        return redirect(reverse(
            "posts:post_detail",
            kwargs={
                "username": self.request.user.username,
                "post_pk": post.pk,
            },
        ))


class CommentView(LoginRequiredMixin, generic.View):
    def post(self, request, post_pk):
        comment_form = CommentModelForm(data=request.POST)
        if not comment_form.is_valid():
            return JsonResponse(comment_form.errors)
        # Add the comment's post and owner before saving it
        comment = comment_form.save(commit=False)
        comment.post = get_object_or_404(Post, pk=post_pk)
        comment.owner = self.request.user
        comment.save()
        return redirect(reverse(
            "posts:post_detail",
            kwargs={
                "username": self.request.user.username,
                "post_pk": post_pk,
            },
        ))


class PostCommentsView(LoginRequiredMixin, generic.View):
    def get(self, request, post_pk):
        """ Get the queryset of comments and paginate it, then, return the requested page number """
        # QuerySet
        comments = Comment.objects.filter(
            post=get_object_or_404(Post, pk=post_pk),
        ).select_related().order_by("-created_at")
        # Paginator
        paginator = Paginator(comments, 2, allow_empty_first_page=True)
        # Page number
        page_number = request.GET.get("page", False)
        if (page_number):
            page_obj = paginator.get_page(page_number)
        else:
            page_obj = paginator.get_page(1)
        return JsonResponse({
            "commentsChunk": list(page_obj.object_list.values()),
            "hasNext": page_obj.has_next(),
            "pageNumber": page_obj.number,
            "commentsCount": paginator.count,
        })


class PostLikesView(LoginRequiredMixin, generic.View):
    def get(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        likes = post.likes.count()
        return JsonResponse({"likes": likes})

    def post(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        like_obj = Like(post=post, owner=self.request.user)
        like_obj.save()
        return redirect(reverse("posts:post_likes", kwargs={"post_pk": post_pk}))


class PostDislikeView(LoginRequiredMixin, generic.View):
    def post(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        Like.objects.get(post=post, owner=self.request.user).delete()
        return redirect(reverse("posts:post_likes", kwargs={"post_pk": post_pk}))
