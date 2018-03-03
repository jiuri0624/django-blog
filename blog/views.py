import markdown
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category
from comments.forms import CommentForm

# Create your views here.

# 改用下面类方法实现
# def index(request):
#     # return HttpResponse('hello blog')
#     post_list = Post.objects.all()
#     return render(request, 'blog/index.html', {'post_list':post_list})
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    contex_object_name = 'post_list'


# 改用下面类方法实现
# def archives(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
#     return render(request, 'blog/index.html', {'post_list':post_list})
class ArchivesView(IndexView):
    def get_queryset(self):
        return super(ArchivesView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'), created_time__month=self.kwargs.get('month'))


# 改用下面类方法实现
# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request, 'blog/index.html', {'post_list':post_list})
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


# 改用下面类方法实现
# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.update_view()
#     post.body = markdown.markdown(post.body, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.toc'])
#     form = CommentForm()
#     comment_list = post.comment_set.all()
#     return render(request, 'blog/detail.html', {'post':post, 'form':form, 'comment_list':comment_list})
class DetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    contex_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(DetailView, self).get(request, *args, **kwargs)
        self.object.update_view()
        return response
    
    def get_object(self, queryset=None):
        post = super(DetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.toc'])
        return post
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({'form':form, 'comment_list':comment_list})
        return context

