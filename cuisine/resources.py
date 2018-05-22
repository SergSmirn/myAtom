from import_export import resources
from .models import Ingredient, Dish


class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient


class DishResource(resources.ModelResource):
    class Meta:
        model = Dish
