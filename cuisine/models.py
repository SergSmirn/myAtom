from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from activity.models import Like


class Ingredient(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    description = models.TextField(blank=True, null=True)
    picture_file = models.ImageField(upload_to='uploads/ingredients', default="default.jpg")

    def __str__(self):
        return self.name


class Dish(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)
    name = models.CharField(max_length=50, db_index=True)
    description = models.TextField()
    picture_file = models.ImageField(upload_to='uploads/dishes', default="default.jpg")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    likes = GenericRelation('activity.Like', related_query_name='dishes')

    def __str__(self):
        return self.name
