from django.db.models import Count
from django.template import Library

from a_common.utils import HtmxHttpRequest
from a_psat import models as psat_models, utils

register = Library()


@register.inclusion_tag('_includes/_sidebar_psat.html')
def sidebar_psat_view(request: HtmxHttpRequest):
    filterset = utils.get_filterset(request)
    top_likes = (
        psat_models.Problem.objects
        .prefetch_related('like_users')
        .annotate(num_likes=Count('like_users'))
        .filter(num_likes__gt=0).order_by('-num_likes')
    )
    elided_page_range = utils.get_elided_page_range(request)

    context = {
        'form': filterset.form,
        'top_likes': top_likes,
        'elided_page_range': elided_page_range,
    }
    return context
