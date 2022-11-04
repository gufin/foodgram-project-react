from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from recipes.models import Recipe
from .serializers import UserRecipeSerializer

User = get_user_model()


def shopping_cart_favorite_update(action_type, request, **kwargs):
    user = request.user
    recipe = get_object_or_404(Recipe, id=kwargs['id'])
    mark = False
    if action_type == 'cart':
        mark = User.objects.filter(id=user.id, cart__recipes=recipe).exists()
    if action_type == 'favorite':
        mark = User.objects.filter(
            id=user.id,
            favourite_recipes=recipe).exists()
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
