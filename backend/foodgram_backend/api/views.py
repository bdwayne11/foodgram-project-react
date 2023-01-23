from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import (TagSerializer, IngredientsSerializer,
                          RecipeSerializer, ShortRecipesSerializer)
from recepts.models import Tag, Ingredients, Recipe, Favourites, Basket
from .filters import RecipeFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, **kwargs):

        if request.method == 'POST':
            return self.add_in(Favourites, self.kwargs.get('pk'), request.user)

        if request.method == 'DELETE':
            return self.delete_from(Favourites, self.kwargs.get('pk'), request.user)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, **kwargs):

        if request.method == 'POST':
            return self.add_in(Basket, self.kwargs.get('pk'), request.user)

        if request.method == 'DELETE':
            return self.delete_from(Basket, self.kwargs.get('pk'), request.user)

    def add_in(self, model, recipe_id, user):
        if model.objects.filter(user=user, recipe__id=recipe_id):
            return Response({'error': 'Такой рецепт уже есть в корзине!'})
        recipe = get_object_or_404(Recipe, id=recipe_id)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipesSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, recipe_id, user):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        basket = model.objects.filter(user=user, recipe__id=recipe_id)
        if not basket.exists():
            return Response({'error': 'Данный рецепт уже удален из корзины.'},
                            status=status.HTTP_400_BAD_REQUEST)
        basket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
