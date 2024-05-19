from django.db.models import Count
from django.template import Library

from a_posts import models as post_models

register = Library()

@register.inclusion_tag('_includes/_sidebar.html')
def sidebar_view(tag=None, user=None):
    categories = post_models.Tag.objects.all()
    top_posts = post_models.Post.objects.annotate(
        num_likes=Count('likes')
    ).filter(num_likes__gt=0).order_by('-num_likes')
    top_comments = post_models.Comment.objects.annotate(
        num_likes=Count('likes')
    ).filter(num_likes__gt=0).order_by('-num_likes')
    context = {
        'categories': categories,
        'tag': tag,
        'top_posts': top_posts,
        'top_comments': top_comments,
        'user': user,
    }
    return context
