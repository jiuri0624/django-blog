from django.shortcuts import render
# from django.http import HttpResponse

from .models import Post

# Create your views here.


def index(request):
    # return HttpResponse('hello blog')
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', {'post_list':post_list})