from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    SAFE_METHODS,
)
from rest_framework import viewsets, status
from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    Favorite,
    IngredientRecipe,
    ShoppingCart
)
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from users.models import User, Subscribe
from .serializers import (
    RecipeReadSerializer,
    RecipeWriteSerializer,
    RecipeShortSerializer,
    TagSerializer,
    IngredientSerializer,
    ShoppingCartSerializer,
    SubscribeSerializer,
    UserSerializer,
    AvatarSerializer,
    FavoriteSerializer
)
from .filters import RecipeFilter


class RecipeViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly | IsAdminOrReadOnly,)
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    model = Recipe

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def add_obj(self, request, pk, serializer):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = serializer(data={
            'user': request.user.id,
            'recipe': recipe.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(RecipeShortSerializer(recipe).data,
                        status=status.HTTP_201_CREATED)

    def delete_obj(self, request, pk, model):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        obj = get_object_or_404(model, recipe=recipe, user=user)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST', 'DELETE'],
            detail=True,
            serializer_class=FavoriteSerializer)
    def favorite(self, request, pk):
        favorite_obj = Favorite.objects.filter(
            user_id=request.user.id,
            recipe_id=pk).exists()
        if request.method == 'POST':
            if not favorite_obj:
                return self.add_obj(request, pk, self.serializer_class)
            return Response(
                {"detail": "Рецепт уже добавлен в избранеое"},
                status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            if favorite_obj:
                return self.delete_obj(request, pk, Favorite)
            return Response(
                {"detail": "Рецепт уже был удален из избранного"},
                status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST', 'DELETE'],
            detail=True,
            serializer_class=ShoppingCartSerializer)
    def shopping_cart(self, request, pk):
        shopping_cart_obj = ShoppingCart.objects.filter(
            user_id=request.user.id,
            recipe_id=pk
        ).exists()
        if request.method == 'POST':
            if not shopping_cart_obj:
                return self.add_obj(request, pk, self.serializer_class)
            return Response(
                {"detail": "Рецепт уже добавлен в корзину"},
                status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            if shopping_cart_obj:
                return self.delete_obj(request, pk, ShoppingCart)
            return Response(
                {"detail": "Рецепт уже был удален из корзины"},
                status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        today = datetime.today()
        shopping_list = (
            f'Список покупок для: {user.get_full_name()}\n\n'
            f'Дата: {today:%Y-%m-%d}\n\n'
        )
        shopping_list += '\n'.join([
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ])
        filename = f'{user.username}_shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    @action(detail=True,
            methods=['GET'],
            url_path='get-link',
            url_name='get-link',
            permission_classes=(AllowAny,))
    def get_short_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        short_link = request.build_absolute_uri(
            reverse('recipes:short_link', args=[recipe.pk])
        )
        return Response({'short-link': short_link}, status=status.HTTP_200_OK)


class TagViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class IngredientViewset(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['^name']
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None


class UserViewSet(UserViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == "me":
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    @action(
        methods=['PUT'],
        permission_classes=(IsAuthenticated,),
        url_path='me/avatar',
        serializer_class=AvatarSerializer,
        detail=False,
    )
    def avatar(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @avatar.mapping.delete
    def delete_avatar(self, request):
        request.user.avatar = None
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)
        if request.method == 'POST':
            serializer = SubscribeSerializer(
                author,
                data=request.data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            subscription = get_object_or_404(Subscribe,
                                             user=user,
                                             author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscribing__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
