from django.urls import path, include
from rest_framework import routers
from .views import (TagViewSet, IngredientsViewSet,
                    RecipeViewSet)
from users.views import CustomUserViewSet

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('recipes', RecipeViewSet)
router.register('users', CustomUserViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    # path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]


