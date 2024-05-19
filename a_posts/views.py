import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from a_posts import forms as post_forms
from a_posts import models as post_models


def home_view(request, tag=None):
    if tag:
        posts = post_models.Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(post_models.Tag, slug=tag)
    else:
        posts = post_models.Post.objects.all()

    paginator = Paginator(posts, per_page=3)
    page = int(request.GET.get('page', 1))
    try:
        posts = paginator.page(page)
    except EmptyPage:
        return HttpResponse('')

    context = {
        'posts': posts,
        'tag': tag,
        'page': page,
    }
    if request.htmx:
        return render(request, 'snippets/loop_home_posts.html', context)
    return render(request, 'a_posts/home.html', context)


@login_required
def post_create_view(request):
    form = post_forms.PostCreateForm()

    if request.method == 'POST':
        form = post_forms.PostCreateForm(request.POST)
        if form.is_valid:
            post = form.save(commit=False)

            website = requests.get(form.data['url'])
            source_code = BeautifulSoup(website.text, 'html.parser')

            find_image = source_code.select('meta[content^="https://live.staticflickr.com/"]')
            image = find_image[0]['content']
            post.image = image

            find_title = source_code.select('h1.photo-title')
            title = find_title[0].text.strip()
            post.title = title

            find_artist = source_code.select('a.owner-name')
            artist = find_artist[0].text.strip()
            post.artist = artist

            post.author = request.user

            post.save()
            form.save_m2m()
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request, 'a_posts/post_create.html', context)


@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(post_models.Post, pk=pk, author=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted')
        return redirect('home')

    context = {
        'post': post,
    }
    return render(request, 'a_posts/post_delete.html', context)


@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(post_models.Post, pk=pk, author=request.user)
    form = post_forms.PostEditForm(instance=post)

    if request.method == 'POST':
        form = post_forms.PostEditForm(request.POST, instance=post)
        if form.is_valid:
            form.save()
            messages.success(request, 'Post updated')
            return redirect('home')

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'a_posts/post_edit.html', context)


def post_page_view(request, pk):
    post = get_object_or_404(post_models.Post, pk=pk)

    comment_form = post_forms.CommentCreateForm()
    reply_form = post_forms.ReplyCreateForm()

    if request.htmx:
        if 'top' in request.GET:
            # comments = post.comments.filter(likes__isnull=False).distinct()
            comments = post.comments.annotate(
                num_likes=Count('likes')
            ).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments = post.comments.all()
        context = {
            'comments': comments,
            'reply_form': reply_form,
        }
        return render(request, 'snippets/loop_post_page_comment.html', context)

    context = {
        'post': post,
        'comment_form': comment_form,
        'reply_form': reply_form,
    }
    return render(request, 'a_posts/post_page.html', context)


@login_required
def comment_sent(request, pk):
    post = get_object_or_404(post_models.Post, pk=pk)
    reply_form = post_forms.ReplyCreateForm()

    if request.method == 'POST':
        form = post_forms.CommentCreateForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
            context = {
                'comment': comment,
                'post': post,
                'reply_form': reply_form,
            }
            return render(request, 'snippets/add_comment.html', context)


@login_required
def comment_delete_view(request, pk):
    comment = get_object_or_404(post_models.Comment, pk=pk, author=request.user)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted')
        return redirect('post', comment.parent_post.id)

    context = {
        'comment': comment,
    }
    return render(request, 'a_posts/comment_delete.html', context)


@login_required
def reply_sent(request, pk):
    comment = get_object_or_404(post_models.Comment, pk=pk)
    reply_form = post_forms.ReplyCreateForm()

    if request.method == 'POST':
        form = post_forms.ReplyCreateForm(request.POST)
        if form.is_valid:
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()
            context = {
                'reply': reply,
                'comment': comment,
                'reply_form': reply_form,
            }
            return render(request, 'snippets/add_reply.html', context)


@login_required
def reply_delete_view(request, pk):
    reply = get_object_or_404(post_models.Reply, pk=pk, author=request.user)

    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply deleted')
        return redirect('post', reply.parent_comment.parent_post.id)

    context = {
        'reply': reply,
    }
    return render(request, 'a_posts/reply_delete.html', context)


def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            pk = kwargs.get('pk')
            post = get_object_or_404(model, pk=pk)
            user_exists = post.likes.filter(username=request.user.username).exists()

            if post.author != request.user:
                if user_exists:
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)

            return func(request, post)
        return wrapper
    return inner_func


@login_required
@like_toggle(post_models.Post)
def like_post(request, post):
    return render(request, 'snippets/likes.html', {'post': post})


@login_required
@like_toggle(post_models.Comment)
def like_comment(request, comment):
    return render(request, 'snippets/likes_comment.html', {'comment': comment})


@login_required
@like_toggle(post_models.Reply)
def like_reply(request, reply):
    return render(request, 'snippets/likes_reply.html', {'reply': reply})
