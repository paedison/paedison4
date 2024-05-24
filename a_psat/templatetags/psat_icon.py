from django.contrib.auth.models import User
from django.template import Library, Node

from a_common.constants import icon_set
from a_psat import models as psat_models

register = Library()


@register.inclusion_tag('a_psat/snippets/likes.html')
def tag_icon_like(user, problem: psat_models.Problem):
    user_exists = user in problem.like_users.all()
    icon_like = icon_set.ICON_LIKE[f'{user_exists}']
    return {
        'user': user,
        'problem': problem,
        'icon_like': icon_like,
    }


@register.inclusion_tag('a_psat/snippets/rates.html')
def tag_icon_rate(user: User, problem: psat_models.Problem):
    rating = 0
    if user in problem.rate_users.all():
        # rate = problem.problemrate_set.objects.filter(user=user).first()
        # rating = rate.rating if rate else 0
        rating = problem.problemrate_set.filter(user=user).first().rating
    icon_rate = icon_set.ICON_RATE[f'star{rating}']
    return {
        'user': user,
        'problem': problem,
        'icon_rate': icon_rate,
    }


@register.filter
def subtract(value, arg) -> int:  # Subtract arg from value
    return arg - int(value)


# @register.simple_tag
# def icon_rate(user, problem: psat_models.Problem):
#     if user in problem.rates.all():
#         rate: psat_models.ProblemRate = psat_models.ProblemRate.objects.filter(
#             user=user, problem=problem).first()
#         rating = rate.rating if rate else 0
#     else:
#         rating = 0
#     return icon_set.ICON_RATE[f'star{rating}']


@register.simple_tag
def icon_solve(user, problem: psat_models.Problem):
    user_exist = user in problem.solves.all()
    if user in problem.solves.all():
        solve: psat_models.ProblemSolve = psat_models.ProblemSolve.objects.filter(
            user=user, problem=problem).first()
        is_correct = solve.is_correct
        return icon_set.ICON_SOLVE[f'{is_correct}']

    return icon_set.ICON_SOLVE['None']
