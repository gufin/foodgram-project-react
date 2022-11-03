from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import Ingredient, Recipe, Tag
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagSerializer, UserRecipeSerializer)
from .shopping_list_generator import generate_shopping_list

User = get_user_model()


class TagRetrieveViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('author').prefetch_related(
        'ingredients'
    ).all()
    serializer_class = RecipeSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    ]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.data.get('author') != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    @action(
        detail=False,
        methods=['post', 'delete'],
        url_path=r'(?P<id>[\d]+)/favorite',
        url_name='favorite',
        pagination_class=None,
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, **kwargs):
        return shopping_cart_favorite_update('favorite', request, **kwargs)

    @action(
        detail=False,
        methods=['post', 'delete'],
        url_path=r'(?P<id>[\d]+)/shopping_cart',
        url_name='shopping_cart',
        pagination_class=None,
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, **kwargs):
        return shopping_cart_favorite_update('cart', request, **kwargs)

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        pagination_class=None,
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        return generate_shopping_list(user)


def shopping_cart_favorite_update(action_type, request, **kwargs):
    user = request.user
    recipe = get_object_or_404(Recipe, id=kwargs['id'])
    mark = False
    if action_type == 'cart':
        mark = User.objects.filter(
                id=user.id,
                cart__recipes=recipe
            ).exists()
    if action_type == 'favorite':
        mark = User.objects.filter(
            id=user.id,
            favourite_recipes=recipe
        ).exists()

    if request.method == 'POST' and not mark:
        if action_type == 'cart':
            user.cart.recipes.add(recipe)
        if action_type == 'favorite':
            recipe.who_likes_it.add(user)
        serializer = UserRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == 'DELETE' and mark:
        if action_type == 'cart':
            user.cart.recipes.remove(recipe)
        if action_type == 'favorite':
            recipe.who_likes_it.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(
        {'detail': 'Действие уже выполнено'},
        status=status.HTTP_400_BAD_REQUEST
    )
