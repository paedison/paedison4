import datetime

import django_filters

from a_psat import models as psat_models

current = datetime
this_year = datetime.date.today().year

CHOICES_YEAR = [
    (year, f'{year}년') for year in reversed(range(2004, this_year + 1))
]
CHOICES_EXAM = (
    ('행시', '5급공채/행정고시'),
    ('입시', '입법고시'),
    ('칠급', '7급공채'),
    ('민경', '민간경력'),
    ('외시', '외교원/외무고시'),
    ('견습', '견습'),
)
CHOICES_SUBJECT = (
    ('헌법', '헌법'),
    ('언어', '언어논리'),
    ('자료', '자료해석'),
    ('상황', '상황판단'),
)
CHOICES_LIKE = (
    ('all', '즐겨찾기 지정'),
    ('true', '즐겨찾기 추가'),
    ('false', '즐겨찾기 제외'),
    ('none', '즐겨찾기 미지정'),
)
CHOICES_RATE = (
    ('all', '난이도 선택'),
    ('5', '★★★★★'),
    ('4', '★★★★☆'),
    ('3', '★★★☆☆'),
    ('2', '★★☆☆☆'),
    ('1', '★☆☆☆☆'),
    ('none', '난이도 미선택'),
)
CHOICES_SOLVE = (
    ('all', '정답 확인'),
    ('true', '맞힌 문제'),
    ('false', '틀린 문제'),
    ('none', '정답 미확인'),
)
CHOICES_MEMO = (
    ('true', '메모 작성'),
    ('none', '메모 미작성'),
)
CHOICES_TAG = (
    ('true', '태그 작성'),
    ('none', '태그 미작성'),
)


class AnonymousPsatFilter(django_filters.FilterSet):
    year = django_filters.ChoiceFilter(
        field_name='year',
        label='',
        empty_label='전체 연도',
        choices=CHOICES_YEAR,
    )
    ex = django_filters.ChoiceFilter(
        field_name='ex',
        label='',
        empty_label='전체 시험',
        choices=CHOICES_EXAM,
    )
    sub = django_filters.ChoiceFilter(
        field_name='sub',
        label='',
        empty_label='전체 과목',
        choices=CHOICES_SUBJECT,
    )

    class Meta:
        model = psat_models.Problem
        fields = ['year', 'ex', 'sub']

    @property
    def qs(self):
        keyword = self.request.GET.get('keyword', '') or self.request.POST.get('keyword', '')
        queryset = super().qs.prefetch_related('like_users', 'rate_users', 'solve_users')
        if keyword:
            return queryset.filter(data__icontains=keyword)
        return queryset


class PsatFilter(AnonymousPsatFilter):
    likes = django_filters.ChoiceFilter(
        label='',
        empty_label='즐겨찾기',
        choices=CHOICES_LIKE,
        method='filter_likes',
    )
    rates = django_filters.ChoiceFilter(
        label='',
        empty_label='난이도',
        choices=CHOICES_RATE,
        method='filter_rates',
    )
    solves = django_filters.ChoiceFilter(
        label='',
        empty_label='정답',
        choices=CHOICES_SOLVE,
        method='filter_solves',
    )
    memos = django_filters.ChoiceFilter(
        label='',
        empty_label='메모',
        choices=CHOICES_MEMO,
        method='filter_memos',
    )
    tags = django_filters.ChoiceFilter(
        label='',
        empty_label='태그',
        choices=CHOICES_TAG,
        method='filter_tags',
    )

    class Meta:
        model = psat_models.Problem
        fields = [
            'year', 'ex', 'sub',
            'likes', 'rates', 'solves', 'memos', 'tags'
        ]

    def filter_likes(self, queryset, name, value):
        filter_dict = {
            'all': queryset.filter(problemlike__isnull=False, like_users=self.request.user),
            'true': queryset.filter(problemlike__is_liked=True, like_users=self.request.user),
            'false': queryset.filter(problemlike__is_liked=False, like_users=self.request.user),
            'none': queryset.exclude(like_users=self.request.user),
        }
        return filter_dict[value]

    def filter_rates(self, queryset, name, value):
        filter_dict = {
            'all': queryset.filter(rate_users__isnull=False, rate_users__user_id=self.request.user.id),
            '1': queryset.filter(rate_users__rating=1, rate_users__user_id=self.request.user.id),
            '2': queryset.filter(rate_users__rating=2, rate_users__user_id=self.request.user.id),
            '3': queryset.filter(rate_users__rating=3, rate_users__user_id=self.request.user.id),
            '4': queryset.filter(rate_users__rating=4, rate_users__user_id=self.request.user.id),
            '5': queryset.filter(rate_users__rating=5, rate_users__user_id=self.request.user.id),
            'none': queryset.exclude(rate_users__user_id=self.request.user.id),
        }
        return filter_dict[value]

    def filter_solves(self, queryset, name, value):
        filter_dict = {
            'all': queryset.filter(solve_users__isnull=False, solve_users__user_id=self.request.user.id),
            'true': queryset.filter(solve_users__is_correct=True, solve_users__user_id=self.request.user.id),
            'false': queryset.filter(solve_users__is_correct=False, solve_users__user_id=self.request.user.id),
            'none': queryset.exclude(solve_users__user_id=self.request.user.id),
        }
        return filter_dict[value]

    def filter_memos(self, queryset, name, value):
        filter_dict = {
            'true': queryset.filter(memo_users__user_id=self.request.user.id),
            'none': queryset.exclude(memo_users__user_id=self.request.user.id),
        }
        return filter_dict[value]

    def filter_tags(self, queryset, name, value):
        filter_dict = {
            'true': queryset.filter(tag_users__user_id=self.request.user.id),
            'none': queryset.exclude(tag_users__user_id=self.request.user.id),
        }
        return filter_dict[value]
