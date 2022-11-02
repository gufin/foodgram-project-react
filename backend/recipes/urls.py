from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientReadOnlyViewSet, RecipeViewSet, TagRetrieveViewSet

router = DefaultRouter()

router.register('tags', TagRetrieveViewSet, basename='tags')
router.register('ingredients', IngredientReadOnlyViewSet,
                basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls))
]
