from django.db import models

from .models import Recipe
from users.models import User


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
        abstracrt = True
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='favorite_shoppingcart_unique'
            )
        ]
