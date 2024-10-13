from django.core.validators import MinValueValidator
from django.db import models

from users.models import User

from .constants import (
    INGREDIENT_MAX_NAME,
    INGREDIENT_MAX_MEASURE_UNIT,
    RECIPE_MAX_NAME,
    TAG_MAX_LENGHT,
)


class Ingredient(models.Model):
    name = models.CharField(
        max_length=INGREDIENT_MAX_NAME,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=INGREDIENT_MAX_MEASURE_UNIT,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='ingredients_unique'
            )
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=TAG_MAX_LENGHT,
        verbose_name='Название'
    )
    slug = models.SlugField(
        null=True,
        max_length=TAG_MAX_LENGHT,
        unique=True,
        verbose_name='слаг'
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='recipes'
    )
    name = models.CharField(
        max_length=RECIPE_MAX_NAME,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='media/'
    )
    text = models.TextField(
        verbose_name='Текстовое описание'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег'
    )
    cooking_time = models.FloatField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(1,
                              message=('Значение не может быть меньше 1'))
        ]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='+'
    )
    amount = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте '


class FavoriteAndShoppingCartModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name="%(class)s_unique'"
            )
        ]


class Favorite(FavoriteAndShoppingCartModel):

    class Meta(FavoriteAndShoppingCartModel.Meta):
        default_related_name = 'favorites'
        verbose_name = 'Избранное'


class ShoppingCart(FavoriteAndShoppingCartModel):

    class Meta(FavoriteAndShoppingCartModel.Meta):
        default_related_name = 'shopping_cart'
        verbose_name = 'Корзина'
