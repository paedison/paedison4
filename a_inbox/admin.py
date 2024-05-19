from django.contrib import admin

from a_inbox import models


class InboxMessageAdmin(admin.ModelAdmin):
    readonly_fields = ('sender', 'conversation', 'body')


admin.site.register(models.InboxMessage, InboxMessageAdmin)
admin.site.register(models.Conversation)
