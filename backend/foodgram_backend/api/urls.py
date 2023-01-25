from django.urls import include, path
from rest_framework import routers

from users.views import CustomUserViewSet

from .views import IngredientsViewSet, RecipeViewSet, TagViewSet

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
