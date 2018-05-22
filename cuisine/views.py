from django.shortcuts import render, redirect, get_object_or_404
from cuisine.models import Dish, Ingredient
from activity.forms import CommentForm
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.generic import TemplateView
from cent import Client, get_timestamp, generate_token


def home(request):
    user = request.user
    if user.is_authenticated:
        dishes = Dish.objects.annotate(likes_count=Count('likes', distinct=True),
                                       favorites_count=Count('favorite', distinct=True),
                                       user_like=Count('likes', filter=Q(likes__author=request.user)),
                                       user_favorite=Count('favorite', filter=Q(favorite__author=request.user))) \
                     .order_by('-likes_count', '-favorites_count', '-user_like', '-user_favorite')[:5]
    else:
        dishes = Dish.objects.annotate(likes_count=Count('likes', distinct=True),
                                       favorites_count=Count('favorite', distinct=True)) \
                     .order_by('-likes_count', '-favorites_count')[:5]
    timestamp = get_timestamp()
    token = generate_token("secret", "", timestamp)
    return render(request, 'home.html', {'dishes': dishes, 'token': token, 'timestamp': timestamp})


def get_dish(request, dish_pk):
    if request.user.is_authenticated:
        dish = Dish.objects.filter(pk=dish_pk).annotate(likes_count=Count('likes', distinct=True),
                                                        favorites_count=Count('favorite', distinct=True),
                                                        user_like=Count('likes', filter=Q(likes__author=request.user)),
                                                        user_favorite=Count('favorite',
                                                                            filter=Q(favorite__author=request.user)))[0]
        comments = dish.comment_set.annotate(likes_count=Count('likes'),
                                             user_like=Count('likes', filter=Q(likes__author=request.user))) \
                       .order_by('-created_at')[:5][::-1]
    else:
        dish = get_object_or_404(Dish, pk=dish_pk)
        comments = dish.comment_set.annotate(likes_count=Count('likes')) \
                       .order_by('-created_at')[:5][::-1]

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.dish_id = dish_pk
            comment.save()
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = CommentForm()
    timestamp = get_timestamp()
    token = generate_token("secret", "", timestamp)
    return render(request, 'dish.html',
                  {'form': form, 'dish': dish, 'comments': comments, 'token': token, 'timestamp': timestamp})


def get_ingredient(request, ingredient_pk):
    ingredient = get_object_or_404(Ingredient, pk=ingredient_pk)
    return render(request, 'ingredient.html', {'ingredient': ingredient})

