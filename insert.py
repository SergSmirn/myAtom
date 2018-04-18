from cuisine.models import Dish, Ingredient, Like
from django.contrib.auth.models import User
from activity.models import Favorite, Comment
from accounts.models import Profile
import datetime
import time
import random


def insert_db():
    count = 100000
    users = (User(username='User name %s' % i,
                  password='password%s' % i, email='User email %s' % i) for i in range(count))
    users = User.objects.bulk_create(users)
    profiles = (Profile(user_id=users[i].pk, city='Moscow', birthday=datetime.date(7, 7, 7)) for i in range(count))
    Profile.objects.bulk_create(profiles)
    ingredients = (Ingredient(name='Ingredient name %s' % i,
                              description='Ingredient description %s' % i) for i in range(count))
    ingredients = Ingredient.objects.bulk_create(ingredients)
    dishes = (Dish(name='Dish name %s' % i, description='Dish description %s' % i,
                   author_id=users[random.randint(0, count - 1)].pk) for i in range(count))
    dishes = Dish.objects.bulk_create(dishes)
    ThroughModel = Dish.ingredients.through
    throughs1 = [ThroughModel(ingredient_id=ingredients[i].pk, dish_id=dishes[i].pk) for i in range(count)]
    throughs2 = [ThroughModel(ingredient_id=ingredients[i].pk,
                              dish_id=dishes[random.randint(i + 1, count - 1)].pk) for i in range(count - 2)]
    throughs1.extend(throughs2)
    ThroughModel.objects.bulk_create(throughs1)
    comments = (Comment(author_id=users[random.randint(0, count - 1)].pk,
                        dish_id=dishes[random.randint(0, count - 1)].pk,
                        text='Comment text %s' % i, ) for i in range(3 * count))
    comments = Comment.objects.bulk_create(comments)
    likes1 = [Like(content_object=comments[random.randint(0, count - 1)],
                   author=users[i]) for i in range(count)]
    likes2 = [Like(content_object=dishes[random.randint(0, count - 1)],
                   author=users[i]) for i in range(count)]
    likes1.extend(likes2)
    Like.objects.bulk_create(likes1)
    favorites = (Favorite(dish=dishes[random.randint(0, count - 1)],
                          author=users[i]) for i in range(count))
    Favorite.objects.bulk_create(favorites)


class timer(object):
    def __init__(self):
        pass

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        print('elapsed time: %f' % self.secs)


with timer():
    insert_db()
