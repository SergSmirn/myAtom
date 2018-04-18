from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Favorite(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey('cuisine.Dish', on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ('author', 'dish')

    def __str__(self):
        return 'On {} by {}'.format(self.dish.name, self.author.username)


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        unique_together = ('author', 'object_id')

    def __str__(self):
        return 'On "{}" by {}'.format(self.content_object, self.author.username)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    dish = models.ForeignKey('cuisine.Dish', on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=200)
    likes = GenericRelation(Like, related_query_name='comments')

    def __str__(self):
        return 'On {} by {}'.format(self.dish.name, self.author.username)
