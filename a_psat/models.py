import os

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.templatetags.static import static
from django.urls import reverse
from taggit.managers import TaggableManager

from _config.settings import BASE_DIR


class Problem(models.Model):
    year = models.IntegerField()

    ex = models.CharField(max_length=2)
    exam = models.CharField(max_length=10)
    exam_label = models.CharField(max_length=20)

    sub = models.CharField(max_length=2)
    subject = models.CharField(max_length=10)

    number = models.IntegerField()
    answer = models.IntegerField()
    question = models.TextField()
    data = models.TextField()

    open_users = models.ManyToManyField(User, related_name='opened_problems', through='ProblemOpen')
    like_users = models.ManyToManyField(User, related_name='liked_problems', through='ProblemLike')
    rate_users = models.ManyToManyField(User, related_name='rated_problems', through='ProblemRate')
    solve_users = models.ManyToManyField(User, related_name='solved_problems', through='ProblemSolve')
    memo_users = models.ManyToManyField(User, related_name='memoed_problems', through='ProblemMemo')
    tag_users = models.ManyToManyField(User, related_name='tagged_problems', through='ProblemTag')
    comment_users = models.ManyToManyField(User, related_name='commented_problems', through='ProblemComment')
    collection_users = models.ManyToManyField('Collection', related_name='collected_problems', through='ProblemCollection')

    class Meta:
        ordering = ['-year', 'id']

    def __str__(self):
        return f'{self.year_ex_sub}({self.id})'

    def get_absolute_url(self):
        return reverse('psat:problem', args=[self.id])

    @property
    def year_ex_sub(self):
        return f'{self.year}{self.ex}{self.sub}'

    @property
    def full_reference(self):
        return f'{self.year}년 {self.exam} {self.subject} {self.number}번'

    @property
    def images(self) -> dict:
        def get_image_path_and_name(number):
            filename = f'PSAT{self.year_ex_sub}{self.number:02}-{number}.png'
            image_exists = os.path.exists(
                os.path.join(BASE_DIR, 'static', 'image', 'PSAT', str(self.year), filename))
            path = name = ''
            if number == 1:
                path = static('image/preparing.png')
                name = 'Preparing Image'
            if image_exists:
                path = static(f'image/PSAT/{self.year}/{filename}')
                name = f'Problem Image {number}'
            return path, name

        path1, name1 = get_image_path_and_name(1)
        path2, name2 = get_image_path_and_name(2)
        return {'path1': path1, 'path2': path2, 'name1': name1, 'name2': name2}


class ProblemOpen(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}[Open]: {self.problem}'


class ProblemLike(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}[Like]: {self.problem}'


class ProblemRate(models.Model):
    class Ratings(models.IntegerChoices):
        STAR1 = 1, '⭐️'
        STAR2 = 2, '⭐️⭐️'
        STAR3 = 3, '⭐️⭐️⭐️'
        STAR4 = 4, '⭐️⭐️⭐️⭐️'
        STAR5 = 5, '⭐️⭐️⭐️⭐️⭐️'

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=Ratings.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}[Rate]: {self.problem}'


class ProblemSolve(models.Model):
    class Answers(models.IntegerChoices):
        ANSWER1 = 1, '①'
        ANSWER2 = 2, '②'
        ANSWER3 = 3, '③'
        ANSWER4 = 4, '④'
        ANSWER5 = 5, '⑤'

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.IntegerField(choices=Answers.choices)
    is_correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}[Solve]: {self.problem}'


class ProblemMemo(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    memo = RichTextField(config_name='minimal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}[Memo]: {self.problem}'


class ProblemTag(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}[Tag]: {self.problem}'


class ProblemComment(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=100)
    comment = RichTextField(config_name='minimal')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='reply_comments')
    hit = models.IntegerField(default=1, verbose_name='조회수')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}: {self.problem}'


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user_id', 'order']
        unique_together = [["user_id", "title"]]

    def __str__(self):
        title = f'[User{self.user_id}_Col{self.id}] {self.title}'
        return title


class ProblemCollection(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='collection_items')
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['collection__user_id', 'collection', 'order']

    def __str__(self):
        return f'{self.collection} - {self.problem}'

    def set_active(self):
        self.is_active = True
        self.save()

    def set_inactive(self):
        self.is_active = False
        self.save()
