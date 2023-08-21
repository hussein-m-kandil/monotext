from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.serializers import serialize
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostModelForm, CommentModelForm
from .models import Post, Comment

# Create your views here.


class IndexView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = "posts/index.html"

    def get_queryset(self):
        return super().get_queryset().order_by("-updated_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_form"] = PostModelForm()
        context["comment_form"] = CommentModelForm()
        return context


class PostView(LoginRequiredMixin, generic.View):
    def get(self, request, post_pk):
        return render(
            request,
            "posts/post_detail.html",
            {"post": get_object_or_404(Post, pk=post_pk)},
        )

    def post(self, request):
        post_form = PostModelForm(data=request.POST)
        if not post_form.is_valid():
            return JsonResponse(post_form.errors)
        # Add the post's owner before saving it
        post = post_form.save(commit=False)
        post.owner = self.request.user
        post.save()
        return redirect(reverse("posts:post_detail", kwargs={"post_pk": post.pk}))


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
        return redirect(reverse("posts:post_detail", kwargs={"post_pk": post_pk}))


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
