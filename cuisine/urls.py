from django.urls import path
from cuisine import views as cuisine_views


urlpatterns = [
    path('dish/<dish_pk>', cuisine_views.get_dish, name='get_dish'),
    path('ingredient/<ingredient_pk>', cuisine_views.get_ingredient, name='get_ingredient'),
]