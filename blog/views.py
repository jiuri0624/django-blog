import markdown
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag
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
    paginate_by =5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context
    
    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range
        right = page_range[page_number:page_number + 2]
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
        if right:
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        if left:
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        data = {
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last':last,
        }
        return data




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


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)



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
        md = markdown.Markdown(extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.toc'])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({'form':form, 'comment_list':comment_list})
        return context

