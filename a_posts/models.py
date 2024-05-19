import uuid

from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=500)
    artist = models.CharField(max_length=500, null=True)
    url = models.URLField(max_length=500, null=True)
    image = models.URLField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_posts', through='LikedPost')
    tags = models.ManyToManyField('Tag')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(
        max_length=100, default=uuid.uuid4,
        unique=True, primary_key=True, editable=False,
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-created']


class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.post.title}'


class Tag(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField(upload_to='icons/', null=True, blank=True)
    slug = models.SlugField(max_length=20, unique=True)
    order = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name='liked_comments', through='LikedComment')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(
        max_length=100, default=uuid.uuid4,
        unique=True, primary_key=True, editable=False,
    )

    def __str__(self):
        author = self.author.username if self.author else 'No author'
        return f'{author}: {self.body[:30]}'

    class Meta:
        ordering = ['-created']


class LikedComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.comment.body[:30]}'


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='replies')
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name='liked_replies', through='LikedReply')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(
        max_length=100, default=uuid.uuid4,
        unique=True, primary_key=True, editable=False,
    )

    def __str__(self):
        author = self.author.username if self.author else 'No author'
        return f'{author}: {self.body:30}'

    class Meta:
        ordering = ['-created']
        verbose_name_plural = "replies"


class LikedReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.reply.body[:30]}'
