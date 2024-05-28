from django.urls import path

from a_psat.views import *

app_name = 'psat'

urlpatterns = [
    path('', index_view, name='index'),
    path('page/', page_filter, name='page-filter'),
    path('category/<tag>/', index_view, name='category'),

    path('problem/<pk>/', problem_view, name='problem'),
    path('problem/like/<pk>/', like_problem, name='like-problem'),
    path('problem/rate/<pk>/', rate_problem, name='rate-problem'),
    path('problem/solve/<pk>/', solve_problem, name='solve-problem'),
    path('problem/tag/add/<pk>/', tag_problem_add, name='tag-problem-add'),
    path('problem/tag/remove/<pk>/', tag_problem_remove, name='tag-problem-remove'),
]
