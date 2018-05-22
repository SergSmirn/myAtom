from django.contrib import admin
from .models import Dish, Ingredient, Like
from activity.models import Comment, Favorite
from accounts.models import Profile
from import_export.admin import ImportExportModelAdmin


@admin.register(Dish)
class PersonAdmin(ImportExportModelAdmin):
    pass


@admin.register(Ingredient)
class PersonAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Profile)