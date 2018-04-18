from django.contrib import admin
from .models import Dish, Ingredient, Like
from activity.models import Comment, Favorite
from accounts.models import Profile


admin.site.register(Dish)
admin.site.register(Ingredient)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Profile)