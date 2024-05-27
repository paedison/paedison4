from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from a_common.constants import icon_set
from a_psat import models as psat_models, utils


def index_view(request, tag=None):
    filterset = utils.get_filterset(request)
    paginator = Paginator(filterset.qs, per_page=10)

    page = int(request.GET.get('page', 1))
    next_path = utils.get_page_added_path(request, page)['next_path']
    elided_page_range = utils.get_elided_page_range(
        request, filterset, page, paginator.num_pages)

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
        return render(
            request, 'a_psat/snippets/loop_home_problems.html', context)
    return render(request, 'a_psat/index.html', context)


def page_filter(request):
    filterset = utils.get_filterset(request)
    paginator = Paginator(filterset.qs, per_page=10)
    page = int(request.GET.get('page', 1))
    elided_page_range = utils.get_elided_page_range(
        request, filterset, page, paginator.num_pages)
    context = {
        'form': filterset.form,
        'page': page,
        'elided_page_range': elided_page_range,
    }
    return render(request, 'a_psat/_includes/_sidebar_psat.html', context)


def problem_view(request, pk):
    queryset = psat_models.Problem.objects.prefetch_related(
        'problemlike_set', 'problemrate_set', 'problemsolve_set',
        'like_users', 'rate_users', 'solve_users',
    )
    problem = get_object_or_404(queryset, pk=pk)
    utils.get_problem_images(problem)
    context = {
        'problem': problem
    }
    if request.htmx:
        return render(request, 'a_psat/_layouts/_b.html#htmx_page', context)
    return render(request, 'a_psat/problem_page.html', context)


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
    return render(request, 'a_psat/snippets/like_result.html', context)


@login_required
def rate_problem(request, pk):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        problem = get_object_or_404(psat_models.Problem, pk=pk)
        user_exists = problem.problemrate_set.filter(user=request.user).exists()
        if user_exists:
            problem_rate = psat_models.ProblemRate.objects.get(
                user=request.user, problem=problem)
            problem_rate.rating = rating
            problem_rate.save()
        else:
            problem.rate_users.add(
                request.user, through_defaults={'rating': rating})
        icon_rate = icon_set.ICON_RATE[f'star{rating}']
        return HttpResponse(icon_rate)


@login_required
def solve_problem(request, pk):
    if request.method == 'POST':
        answer = int(request.POST.get('answer'))
        problem = get_object_or_404(psat_models.Problem, pk=pk)
        is_correct = answer == problem.answer

        user_exists = problem.problemsolve_set.filter(user=request.user).exists()
        if user_exists:
            problem_solve = psat_models.ProblemSolve.objects.get(
                user=request.user, problem=problem)
            problem_solve.answer = answer
            problem_solve.is_correct = is_correct
            problem_solve.save()
        else:
            problem.solve_users.add(
                request.user,
                through_defaults={'answer': answer, 'is_correct': is_correct}
            )

        icon_solve = icon_set.ICON_SOLVE[f'{is_correct}']
        message = '정답입니다.' if is_correct else '오답입니다. 다시 풀어보세요.'

        context = {
            'problem': problem,
            'icon_solve': icon_solve,
            'is_correct': is_correct,
            'message': message,
        }
        return render(request, 'a_psat/snippets/solve_result.html', context)


@login_required
def add_problem_tag(request):
    pass
