from allauth.account.views import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from a_users import forms as user_forms
from a_posts import forms as post_forms
from a_inbox import forms as inbox_forms


def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except AttributeError:
            raise Http404()

    posts = profile.user.posts.all()

    if request.htmx:
        if 'top-posts' in request.GET:
            posts = profile.user.posts.annotate(
                num_likes=Count('likes')
            ).filter(num_likes__gt=0).order_by('-num_likes')
        elif 'top-comments' in request.GET:
            comments = profile.user.comments.annotate(
                num_likes=Count('likes')
            ).filter(num_likes__gt=0).order_by('-num_likes')
            reply_form = post_forms.ReplyCreateForm
            context = {
                'comments': comments,
                'reply_form': reply_form,
            }
            return render(request, 'snippets/loop_profile_comments.html', context)
        elif 'liked-posts' in request.GET:
            posts = profile.user.liked_posts.order_by('-likedpost__created')
        return render(request, 'snippets/loop_profile_posts.html', {'posts': posts})

    new_message_form = inbox_forms.InboxNewMessageForm()

    context = {
        'profile': profile,
        'posts': posts,
        'new_message_form': new_message_form,
    }
    return render(request, 'a_users/profile.html', context)


@login_required
def profile_edit_view(request):
    form = user_forms.ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        form = user_forms.ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    if request.path == reverse('profile-onboarding'):
        template_name = 'a_users/profile_onboarding.html'
    else:
        template_name = 'a_users/profile_edit.html'

    context = {
        'form': form,
    }
    return render(request, template_name, context)


@login_required
def profile_delete_view(request):
    user = request.user

    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, what a pity')
        return redirect('home')

    return render(request, 'a_users/profile_delete.html')
