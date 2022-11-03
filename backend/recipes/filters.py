from django.contrib.auth import get_user_model
from django_filters import CharFilter, FilterSet as DefaultFilterSet
from django_filters.rest_framework import filters, FilterSet

from .models import Recipe

User = get_user_model()


class RecipeFilter(FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_in_shopping_cart = filters.BooleanFilter(method='cart_filter')
    is_favorited = filters.BooleanFilter(method='favorite_filter')

    def cart_filter(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(carts__user=self.request.user)
        return queryset

    def favorite_filter(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(who_likes_it__id=self.request.user.id)
        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags']


class IngredientFilter(DefaultFilterSet):
    name = CharFilter(
        field_name='name', lookup_expr='startswith'
    )
