from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (RecipeViewset,
                    TagViewset,
                    IngredientViewset,
                    CustomUserViewSet)

app_name = 'api'

router_V1 = DefaultRouter()
router_V1.register('recipes', RecipeViewset, basename='recipes')
router_V1.register('tags', TagViewset)
router_V1.register('ingredients', IngredientViewset)
router_V1.register('users', CustomUserViewSet)


urlpatterns = [
    path('', include(router_V1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
