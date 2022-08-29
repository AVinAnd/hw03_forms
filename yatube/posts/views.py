from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Post, Group, User
from .forms import PostForm


POSTS_ON_SCREEN = 10
CHARS_IN_TITLE = 30


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, POSTS_ON_SCREEN)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, POSTS_ON_SCREEN)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    username = get_object_or_404(User, username=username)
    post_list = Post.objects.all().filter(author=username)
    paginator = Paginator(post_list, POSTS_ON_SCREEN)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts_by_author = post_list.count()
    context = {
        'username': username,
        'page_obj': page_obj,
        'posts_by_author': posts_by_author,
    }
    return render(request, 'posts/profile.html', context)


def post_details(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    posts_by_author = Post.objects.all().filter(author=post.author).count()
    title = post.text[:CHARS_IN_TITLE]
    context = {
        'post': post,
        'posts_by_author': posts_by_author,
        'title': title,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(f'/profile/{post.author}/')
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


def author_only(func):
    def check_author(request, post_id):
        post = Post.objects.get(pk=post_id)
        if request.user == post.author:
            return func(request, post_id)
        return redirect(f'/posts/{post_id}')
    return check_author


@author_only
def post_edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            edit_post = form.save(commit=False)
            edit_post.id = post.id
            edit_post.pub_date = post.pub_date
            edit_post.author = post.author
            edit_post.save()
            return redirect(f'/posts/{post_id}/')
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm(instance=post)
    is_edit = True
    context = {
        'form': form,
        'is_edit': is_edit,
        'post': post,
    }
    return render(request, 'posts/create_post.html', context)
