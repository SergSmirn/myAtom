from cuisine.models import Ingredient, Like
from django.contrib.auth.models import User
from activity.models import Favorite, Comment
from accounts.models import Profile


User.objects.exclude(pk=7).delete()
Ingredient.objects.all().delete()
