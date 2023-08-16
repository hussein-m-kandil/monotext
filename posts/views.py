from django.shortcuts import render
from django.views import generic

# Create your views here.


class IndexView(generic.View):
    def get(self, request):
        return render(
            request=request,
            template_name="posts/index.html",
            context={},
        )
