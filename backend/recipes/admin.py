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


class IngredientsInline(admin.TabularInline):
    model = IngredientRecipe

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['name'].required = True
        formset.form.base_fields['amount'].required = True
        return formset


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
    inlines = [IngredientsInline,]
    list_display = (
        'author',
        'name',
        'get_tag',
    )
    filter_horizontal = ('tags',)
    search_fields = ('name', 'author__username',)
    list_filter = ('tags',)


admin.site.empty_value_display = 'значение отсутствует'
