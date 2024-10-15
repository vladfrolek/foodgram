from django.contrib import admin

from .models import (
    Tag,
    Recipe,
    IngredientRecipe
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )


@admin.register(IngredientRecipe)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount'
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    def get_tag(self, object):
        """Получает тег или список тегов рецепта."""
        tag_list = object.tags.get_queryset()
        tag_str = ''
        for tag in tag_list:
            tag_str += ', ' + tag.name
        return tag_str.lstrip(', ')

    def get_ingredients(self, object):
        """Получает тег или список тегов рецепта."""
        ingredient_list = object.ingredients.get_queryset()
        ingredient_str = ''
        for ingredient in ingredient_list:
            ingredient_str += ', ' + ingredient.name
        return ingredient_str.lstrip(', ')
    get_tag.short_description = 'Теги'
    list_display = (
        'author',
        'name',
        'get_tag',
    )
    filter_horizontal = ('tags',)
    search_fields = ('name', 'author__username',)
    list_filter = ('tags',)


admin.site.empty_value_display = 'значение отсутствует'
