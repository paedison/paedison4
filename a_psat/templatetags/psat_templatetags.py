from django.contrib.auth.models import User
from django.template import Library, Node

from a_common.constants import icon_set
from a_psat import models as psat_models

register = Library()


@register.inclusion_tag('a_psat/snippets/likes.html')
def container_icon_like(user: User, problem: psat_models.Problem):
    user_exists = user in problem.like_users.all()
    icon_like = icon_set.ICON_LIKE[f'{user_exists}']
    return {
        'user': user,
        'problem': problem,
        'icon_like': icon_like,
    }


@register.inclusion_tag('a_psat/snippets/rates.html')
def container_icon_rate(user: User, problem: psat_models.Problem):
    rating = 0
    if user in problem.rate_users.all():
        rating = problem.problemrate_set.filter(user=user).first().rating
    icon_rate = icon_set.ICON_RATE[f'star{rating}']
    return {
        'user': user,
        'problem': problem,
        'icon_rate': icon_rate,
    }


@register.inclusion_tag('a_psat/snippets/solves.html')
def container_icon_solve(user: User, problem: psat_models.Problem):
    is_correct = None
    if user in problem.solve_users.all():
        is_correct = problem.problemsolve_set.filter(user=user).first().is_correct
    icon_solve = icon_set.ICON_SOLVE[f'{is_correct}']
    return {
        'user': user,
        'problem': problem,
        'icon_solve': icon_solve,
    }


@register.inclusion_tag('a_psat/snippets/tags.html')
def container_problem_tag(user: User, problem: psat_models.Problem):
    tags = []
    if user in problem.tag_users.all():
        tags = list(problem.problemtag_set.get(user=user).tags.names())
    return {
        'user': user,
        'problem': problem,
        'tags': tags,
    }


@register.filter
def subtract(value, arg) -> int:  # Subtract arg from value
    return arg - int(value)
