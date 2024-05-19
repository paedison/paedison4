"""
URL configuration for paedison4 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from a_posts import views as post_views
from a_users import views as user_views

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('check_in_as_boss/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    path('', post_views.home_view, name='home'),
    path('post/category/<tag>/', post_views.home_view, name='category'),
    path('post/create/', post_views.post_create_view, name='post-create'),
    path('post/delete/<pk>/', post_views.post_delete_view, name='post-delete'),
    path('post/edit/<pk>/', post_views.post_edit_view, name='post-edit'),
    path('post/<pk>/', post_views.post_page_view, name='post'),
    path('post/like/<pk>/', post_views.like_post, name='like-post'),
    path('post/comment/sent/<pk>/', post_views.comment_sent, name='comment-sent'),
    path('post/comment/delete/<pk>/', post_views.comment_delete_view, name='comment-delete'),
    path('post/comment/like/<pk>/', post_views.like_comment, name='like-comment'),
    path('post/reply/sent/<pk>/', post_views.reply_sent, name='reply-sent'),
    path('post/reply/delete/<pk>/', post_views.reply_delete_view, name='reply-delete'),
    path('post/reply/like/<pk>/', post_views.like_reply, name='like-reply'),

    path('profile/', user_views.profile_view, name='profile'),
    path('profile/user/<username>/', user_views.profile_view, name='user-profile'),
    path('profile/edit/', user_views.profile_edit_view, name='profile-edit'),
    path('profile/delete/', user_views.profile_delete_view, name='profile-delete'),
    path('profile/onboarding/', user_views.profile_edit_view, name='profile-onboarding'),

    path('inbox/', include('a_inbox.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
