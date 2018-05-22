from django.shortcuts import render, get_object_or_404
from cuisine.models import Dish, Ingredient
from activity.models import Comment
from activity.forms import CommentForm
from django.http import JsonResponse
from django.db.models import Count, Q
import bleach
from cent import Client


url = "http://10.5.126.9:8002"
secret_key = "secret"


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
        type = 'like'
    else:
        obj.likes.get(author=request.user).delete()
        is_liked = False
        type = 'unlike'

    client = Client(url, secret_key, timeout=1)
    data = {"type": type, 'id': obj_pk}
    if obj_type == 'dish':
        client.publish('home', data)
    elif obj_type == 'comment':
        client.publish('comment', data)
    return JsonResponse({'is_liked': is_liked})


def check_favorites(request):
    dish_pk = request.GET['dish_pk']
    dish = get_object_or_404(Dish, pk=dish_pk)
    favorite = dish.favorite_set.filter(author=request.user)
    if not favorite:
        dish.favorite_set.create(author=request.user)
        is_favorited = True
        type = 'favorite'
    else:
        dish.favorite_set.get(author=request.user).delete()
        is_favorited = False
        type = 'unfavorite'
    client = Client(url, secret_key, timeout=1)
    data = {"type": type, 'id': dish_pk}
    client.publish('home', data)
    return JsonResponse({'is_favorited': is_favorited})


def more_dishes(request):
    page = int(request.GET['page'])
    dishes = Dish.objects.annotate(likes_count=Count('likes', distinct=True),
                                   favorites_count=Count('favorite', distinct=True),
                                   user_like=Count('likes', filter=Q(likes__author=request.user)),
                                   user_favorite=Count('favorite', filter=Q(favorite__author=request.user))) \
                 .order_by('-likes_count', '-favorites_count', '-user_like', '-user_favorite')[page * 5:(page + 1) * 5]
    return JsonResponse({'dishes': list(dishes.values('id', 'name', 'author__username', 'likes_count',
                                                      'favorites_count', 'created_at', 'picture_file', 'user_like',
                                                      'user_favorite'))})


def more_comments(request):
    page = int(request.GET['page'])
    dish_pk = int(request.GET['dish_pk'])
    if request.user.is_authenticated:
        dish = Dish.objects.filter(pk=dish_pk).annotate(likes_count=Count('likes', distinct=True),
                                                        favorites_count=Count('favorite', distinct=True),
                                                        user_like=Count('likes', filter=Q(likes__author=request.user)),
                                                        user_favorite=Count('favorite',
                                                                            filter=Q(favorite__author=request.user)))[0]
        comments = dish.comment_set.annotate(likes_count=Count('likes'),
                                             user_like=Count('likes', filter=Q(likes__author=request.user))) \
                       .order_by('-created_at')\
                       .values('id', 'text', 'created_at', 'author__username', 'author__profile__avatar')\
                       [page * 5:(page + 1) * 5]
    else:
        dish = get_object_or_404(Dish, pk=dish_pk)
        comments = dish.comment_set.annotate(likes_count=Count('likes')) \
                       .order_by('-created_at')\
                       .values('id', 'text', 'created_at', 'author__username', 'author__profile__avatar')\
                       [page * 5:(page + 1) * 5]
    return JsonResponse({'comments': list(comments)})


def add_comment(request):
    if request.method == 'POST':
        dish_pk = request.POST.get('dish_id')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.text = bleach.clean(request.POST.get('text'))
            comment.author = request.user
            comment.dish_id = dish_pk
            comment.save()
            data = {'type': 'new-comment','comment_pk': comment.pk, 'text': comment.text, 'author': request.user.username,
                                 'avatar': request.user.profile.avatar.url, 'created_at': str(comment.created_at)}
            client = Client(url, secret_key, timeout=1)
            client.publish('comment', data)
            return JsonResponse({'status': 'ok'})


def delete_comment(request):
    comment_id = request.GET.get('comment_id')
    comment = request.user.comment_set.filter(pk=comment_id)
    if comment:
        comment.delete()
        data = {'type': 'del-comment', 'id': comment_id}
        client = Client(url, secret_key, timeout=1)
        client.publish('comment', data)
        status = 'ok'
    else:
        status = 'error'
    return JsonResponse({'status': status})


def search_ingredients(request):
    query = request.GET.get('query')
    if not query:
        results = []
    else:
        results = Ingredient.objects.filter(name__icontains=query).values('id', 'name')
    return JsonResponse({'results': list(results)})


def search_dishes(request):
    querylist = request.GET.getlist('ingredient_pks[]')
    result = Dish.objects.annotate(likes_count=Count('likes', distinct=True),
                                   favorites_count=Count('favorite', distinct=True),
                                   user_like=Count('likes', filter=Q(likes__author=request.user)),
                                   user_favorite=Count('favorite', filter=Q(favorite__author=request.user))) \
        .order_by('-likes_count', '-favorites_count', '-user_like', '-user_favorite')
    for query in querylist:
        result = result.filter(ingredients=query)
    return JsonResponse({'results': list(result.values('id', 'name', 'author__username', 'likes_count',
                                                      'favorites_count', 'created_at', 'picture_file', 'user_like',
                                                      'user_favorite'))})
