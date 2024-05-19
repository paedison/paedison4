from django.contrib import admin

from a_posts import models

admin.site.register(models.Post)
admin.site.register(models.Tag)
admin.site.register(models.Comment)
admin.site.register(models.Reply)
admin.site.register(models.LikedPost)
admin.site.register(models.LikedComment)
admin.site.register(models.LikedReply)
