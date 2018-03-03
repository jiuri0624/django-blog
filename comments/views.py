from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from blog.models import Post
from .models import Comment
from .forms import CommentForm

# Create your views here.

def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form= CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('blog:detail', args=(post_pk, )))
        else:
            comment_list = post.comment_set.all()
            return render(request, 'blog/detail.html', {'post':post, 'form':form, 'comment_list':comment_list})
    else:
        return HttpResponseRedirect(reverse('blog:detail', args=(post_pk, )))