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
from a_posts import views

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('check_in_as_boss/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    path('', views.home_view, name='home'),
    path('category/<tag>/', views.home_view, name='category'),
    path('post/create/', views.post_create_view, name='post-create'),
    path('post/delete/<pk>/', views.post_delete_view, name='post-delete'),
    path('post/edit/<pk>/', views.post_edit_view, name='post-edit'),
    path('post/<pk>/', views.post_page_view, name='post'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
