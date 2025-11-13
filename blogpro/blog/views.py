from .forms import CommentForm, PostForm
from .models import Post
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from taggit.models import Tag
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='account:login')
def post_list(request, tag_slug=None):
    if tag_slug:
        tag = Tag.objects.filter(slug=tag_slug).first()
        all_post = Post.objects.filter(tags__in=[tag])
    else:
        all_post = Post.objects.all()
    tag_list = Tag.objects.all()
    paginator = Paginator(all_post, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        '../templates/post/list.html',
        {'posts': posts, 'tag_list': tag_list}
    )


@login_required(login_url='account:login')
def my_post_list(request):
    all_post = Post.objects.filter(author=request.user)
    tag_list = Tag.objects.all()
    paginator = Paginator(all_post, 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        '../templates/post/list.html',
        {'posts': posts, 'tag_list': tag_list}
    )


@login_required(login_url='account:login')
def post_detail(request, year, month, day, slug):
    post = Post.objects.filter(
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=slug
    ).first()
    if post is None:
        return render(
            request,
            '../templates/post/no_blog.html'
        )
    else:
        comments = post.comments.filter(active=True)
        new_comment = None
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.commenter = request.user
                new_comment.save()
        comment_form = CommentForm()
        return render(
            request,
            '../templates/post/detail.html',
            {
                'post': post,
                'comments': comments,
                'new_comment': new_comment,
                'comment_form': comment_form
            }
        )


@login_required(login_url='account:login')
def create_blog(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            post_form.save_m2m()
            return redirect('blog:my_post_list')
    else:
        post_form = PostForm()
    return render(
        request,
        '../templates/post/creablog.html',
        {'user_form': post_form, 'hideCreaBlog': True}
    )


@login_required(login_url='account:login')
def blog_update(request, slug=None):
    blog = Post.objects.filter(slug=slug).first()
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=blog)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            post_form.save_m2m()
            return redirect('blog:my_post_list')
    else:
        post_form = PostForm(instance=blog)
    return render(
        request,
        '../templates/post/updateblog.html',
        {'user_form': post_form}
    )


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:my_post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get(self, request, *args, **kwargs):
        """重写GET请求，直接执行删除并跳转，不显示确认模板"""
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, '博客已成功删除！')
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        """处理无权限的情况"""
        messages.error(self.request, '您没有权限删除此博客！')
        return redirect('my_post_list')
