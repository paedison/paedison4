from django.contrib import admin

from a_psat import models

admin.site.register(models.Problem)
admin.site.register(models.ProblemOpen)
admin.site.register(models.ProblemLike)
admin.site.register(models.ProblemRate)
admin.site.register(models.ProblemSolve)
admin.site.register(models.ProblemMemo)
admin.site.register(models.ProblemTag)
admin.site.register(models.ProblemComment)
admin.site.register(models.Collection)
admin.site.register(models.ProblemCollection)
