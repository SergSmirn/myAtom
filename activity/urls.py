from django.urls import path
from activity import views


urlpatterns = [
    path('check_likes/', views.check_likes),
    path('check_favorites/', views.check_favorites),
    path('more_dishes/', views.more_dishes),
    path('more_comments/', views.more_comments),
    path('add_comment/', views.add_comment),
    path('delete_comment/', views.delete_comment),
    path('search_ingredients/', views.search_ingredients),
    path('search_dishes/', views.search_dishes)

]