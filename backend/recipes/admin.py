from django.contrib import admin

from .models import Cart, Ingredient, IngredientAmount, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'measurement_unit',
    ]
    list_filter = [
        'name',
    ]
    search_fields = [
        'name',
    ]
    empty_value_display = '-пусто-'


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'amount',
        'ingredient',
        'recipe',
    ]
    list_filter = [
        'ingredient',
        'recipe',
    ]
    search_fields = [
        'recipe',
    ]
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'color',
        'slug',
    ]
    list_filter = [
        'name',
        'color',
    ]
    search_fields = [
        'name',
    ]
    empty_value_display = '-пусто-'


class TagInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1
    verbose_name = 'Тег'
    verbose_name_plural = 'Теги'


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    fk_name = 'recipe'
    extra = 1
    verbose_name = 'Ингридиент'
    verbose_name_plural = 'Ингридиенты'


class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'image',
        'text',
        'cooking_time',
        'author',
    ]
    exclude = [
        'ingredients',
        'tags',
        'who_likes_it',
    ]
    inlines = [
        IngredientAmountInline,
        TagInline,
    ]
    list_filter = [
        'name',
        'cooking_time',
        'author',
    ]
    search_fields = [
        'name',
        'author',
    ]
    empty_value_display = '-пусто-'


class RecipesInline(admin.StackedInline):
    model = Cart.recipes.through
    extra = 1
    verbose_name = 'Рецепт'
    verbose_name_plural = 'Рецепты'


class CartAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'user',
    ]
    exclude = [
        'recipes',
    ]
    inlines = [
        RecipesInline,
    ]
    list_filter = [
        'user',
    ]
    search_fields = [
        'user',
    ]
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Cart, CartAdmin)
