from django.shortcuts import render, get_object_or_404
from cuisine.models import Dish
from activity.models import Comment
from django.http import JsonResponse
from django.db.models import Count, Q


def check_likes(request):
    obj_pk = request.GET['obj_pk']
    obj_type = request.GET['obj_type']
    if obj_type == 'comment':
        obj = get_object_or_404(Comment, pk=obj_pk)
    elif obj_type == 'dish':
        obj = get_object_or_404(Dish, pk=obj_pk)
    like = obj.likes.filter(author=request.user)
    if not like:
        obj.likes.create(author=request.user)
        is_liked = True
    else:
        obj.likes.get(author=request.user).delete()
        is_liked = False
    likes_count = obj.likes.count()
    return JsonResponse({'likes_count': likes_count, 'is_liked': is_liked})


def check_favorites(request):
    dish_pk = request.GET['dish_pk']
    dish = get_object_or_404(Dish, pk=dish_pk)
    favorite = dish.favorite_set.filter(author=request.user)
    if not favorite:
        dish.favorite_set.create(author=request.user)
        is_favorited = True
    else:
        dish.favorite_set.get(author=request.user).delete()
        is_favorited = False
    favorites_count = dish.favorite_set.count()
    return JsonResponse({'favorites_count': favorites_count, 'is_favorited': is_favorited})


def more_dishes(request):
    page = int(request.GET['page'])
    dishes = Dish.objects.annotate(likes_count=Count('likes', distinct=True),
                                   favorites_count=Count('favorite', distinct=True),
                                   user_like=Count('likes', filter=Q(likes__author=request.user)),
                                   user_favorite=Count('favorite', filter=Q(favorite__author=request.user))) \
                 .order_by('-likes_count', '-favorites_count', '-user_like', '-user_favorite')[page * 10:(page + 1) * 10]
    return JsonResponse({'dishes': list(dishes.values('id', 'name', 'author__username', 'likes_count', 'favorites_count', 'created_at', 'picture_file', 'user_like', 'user_favorite'))})
