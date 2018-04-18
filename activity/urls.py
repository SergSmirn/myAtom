from django.urls import path
from activity import views


urlpatterns = [
    path('check_likes/', views.check_likes, name='check_likes'),
    path('check_favorites/', views.check_favorites, name='check_favorites'),
    path('more/', views.more_dishes, name='more_dishes')
]