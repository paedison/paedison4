from django.urls import path

from a_inbox import views as inbox_views

urlpatterns = [
    path('', inbox_views.inbox_view, name='inbox'),
    path('c/<conversation_id>/', inbox_views.inbox_view, name='inbox'),
    path('search/users/', inbox_views.search_users, name='inbox-search-users'),
    path('new/message/<recipient_id>/', inbox_views.new_message, name='inbox-new-message'),
    path('new/reply/<conversation_id>/', inbox_views.new_reply, name='inbox-new-reply'),
    path('notify/<conversation_id>/', inbox_views.notify_new_message, name='notify-new-message'),
    path('notify-inbox/', inbox_views.notify_inbox, name='notify-inbox'),
]
