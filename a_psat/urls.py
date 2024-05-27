from django.urls import path

from a_psat import views as psat_views

app_name = 'psat'

urlpatterns = [
    path('', psat_views.index_view, name='index'),
    path('page/', psat_views.page_filter, name='page-filter'),
    path('problem/<pk>/', psat_views.problem_view, name='problem'),
    path('category/<tag>/', psat_views.index_view, name='category'),
    path('like/<pk>/', psat_views.like_problem, name='like-problem'),
    path('rate/<pk>/', psat_views.rate_problem, name='rate-problem'),
    path('solve/<pk>/', psat_views.solve_problem, name='solve-problem'),
    path('solve/<pk>/', psat_views.add_problem_tag, name='add-problem-tag'),
]
