from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from constants import USER_MODEL_MAX_LENGTH


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'username',
        'last_name'
    ]

    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты')
    username = models.CharField(
        verbose_name='Никнейм пользователя',
        unique=True,
        max_length=USER_MODEL_MAX_LENGTH,
        validators=[UnicodeUsernameValidator()]
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=USER_MODEL_MAX_LENGTH
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=USER_MODEL_MAX_LENGTH
    )
    avatar = models.ImageField(
        upload_to='media/users/',
        blank=True,
        verbose_name='Аватар Пользователя')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing'
    )

    class Meta:
        constraints = (
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='check_subscribe',
            ),
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow',
            )
        )
        verbose_name = 'Подписка пользователей'
        verbose_name_plural = 'Подписка пользователей'
