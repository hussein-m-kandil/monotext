from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import generic
from .forms import PostModelForm, CommentModelForm
from .models import Post, Comment

# Create your views here.


class IndexView(generic.ListView):
    model = Post
    template_name = "posts/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_form = PostModelForm()
        comment_form = CommentModelForm()
        context["post_form"] = post_form
        context["comment_form"] = comment_form
        return context


class PostView(generic.View):
    def post(self, request):
        post_form = PostModelForm(data=request.POST)
        if not post_form.is_valid():
            return JsonResponse(post_form.errors)
        # TODO: Save the owner before saving the form (after making the fields in the model)
        post_form.save()
        return redirect(reverse("posts:index"))


class CommentView(generic.View):
    def post(self, request, post_pk):
        comment_form = CommentModelForm(date=request.POST)
        if not comment_form.is_valid():
            post_list = Post.objects.all()
            post_form = PostModelForm()
            context = {
                "post_form": post_form,
                "comment_form": comment_form,
                "post_list": post_list,
                "object_list": post_list,
            }
            return render(
                request=request,
                template_name="posts/index.html",
                context=context,
            )
        # TODO: Save the owner before saving the form (after making the fields in the model)
        comment_form.cleaned_data["post"] = get_object_or_404(Post, pk=post_pk)
        comment_form.save()
        return redirect(reverse("posts:index"))
