from django.contrib import admin

from a_posts import models as post_models

admin.site.register(post_models.Post)
admin.site.register(post_models.Tag)
