from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from a_common.constants import icon_set
from a_psat import models as psat_models, utils


def page_filter(request):
    page = int(request.GET.get('page', 1))
    elided_page_range = utils.get_elided_page_range(request)
    context = {
        'page': page,
        'elided_page_range': elided_page_range,
    }
    return render(request, 'a_psat/snippets/page_filter.html', context)


def index_view(request, tag=None):
    filterset = utils.get_filterset(request)
    paginator = Paginator(filterset.qs, per_page=10)

    page = int(request.GET.get('page', 1))
    elided_page_range = utils.get_elided_page_range(request, filterset, page)
    next_path = utils.get_page_added_path(request, page)['next_path']

    try:
        problems = paginator.page(page)
    except EmptyPage:
        return HttpResponse('')

    context = {
        'problems': problems,
        'tag': tag,
        'form': filterset.form,
        'next_path': next_path,
        'page': page,
        'elided_page_range': elided_page_range,
    }
    if request.htmx:
        return render(request, 'a_psat/snippets/loop_home_problems.html', context)
    return render(request, 'a_psat/index.html', context)


@login_required
def like_problem(request, pk):
    problem = get_object_or_404(psat_models.Problem, pk=pk)
    user_exists = problem.problemlike_set.filter(user=request.user).exists()
    if user_exists:
        problem.like_users.remove(request.user)
    else:
        problem.like_users.add(request.user)
    icon_like = icon_set.ICON_LIKE[f'{not user_exists}']
    context = {
        'problem': problem,
        'icon_like': icon_like,
    }
    return render(request, 'a_psat/snippets/likes.html', context)


@login_required
def rate_problem(request, pk):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        problem = get_object_or_404(psat_models.Problem, pk=pk)
        user_exists = problem.problemrate_set.filter(user=request.user).exists()
        print(user_exists)
        if user_exists:
            problem_rate = psat_models.ProblemRate.objects.get(user=request.user, problem=problem)
            problem_rate.rating = rating
            problem_rate.save()
        else:
            test = problem.rate_users.add(request.user, through_defaults={'rating': rating})
            print(test)
        icon_rate = icon_set.ICON_RATE[f'star{rating}']
        return HttpResponse(icon_rate)
