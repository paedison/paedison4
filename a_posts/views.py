from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from bs4 import BeautifulSoup
import requests

from a_posts import forms as post_forms
from a_posts import models as post_models


def home_view(request, tag=None):
    if tag:
        posts = post_models.Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(post_models.Tag, slug=tag)
    else:
        posts = post_models.Post.objects.all()

    categories = post_models.Tag.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
        'tag': tag,
    }
    return render(request, 'a_posts/home.html', context)


def post_create_view(request):
    form = post_forms.PostCreateForm()

    if request.method == 'POST':
        form = post_forms.PostCreateForm(request.POST)
        if form.is_valid():
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

            post.save()
            form.save_m2m()
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request, 'a_posts/post_create.html', context)


def post_delete_view(request, pk):
    post = get_object_or_404(post_models.Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted')
        return redirect('home')

    context = {
        'post': post,
    }
    return render(request, 'a_posts/post_delete.html', context)


def post_edit_view(request, pk):
    post = get_object_or_404(post_models.Post, pk=pk)
    form = post_forms.PostEditForm(instance=post)

    if request.method == 'POST':
        form = post_forms.PostEditForm(request.POST, instance=post)
        if form.is_valid():
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
    context = {
        'post': post,
    }
    return render(request, 'a_posts/post_page.html', context)
