
from django.contrib import admin

from .models import Tag, Problem


# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    pass