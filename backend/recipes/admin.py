from django.contrib import admin

from .models import (
    Tag,
    Recipe,
    Ingredient,
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
    get_tag.short_description = 'Теги'
    list_display = (
        'author',
        'name',
        'get_tag',
    )
    filter_horizontal = ('tags',)
    search_fields = ('name', 'author__username',)
    list_filter = ('tags',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)


admin.site.empty_value_display = 'значение отсутствует'
