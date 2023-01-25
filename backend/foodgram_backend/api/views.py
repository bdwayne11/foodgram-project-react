from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recepts.models import (Basket, Favourites, Ingredients,
                            IngredientsRecipes, Recipe, Tag)

from .filters import IngredientSearchFilter, RecipeFilter
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (IngredientsSerializer, RecipeSerializer,
                          ShortRecipesSerializer, TagSerializer,
                          WriteRecipesSerializer)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAdminOrReadOnly | IsAuthorOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return WriteRecipesSerializer

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
            return self.delete_from(Favourites,
                                    self.kwargs.get('pk'), request.user)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, **kwargs):

        if request.method == 'POST':
            return self.add_in(Basket, self.kwargs.get('pk'), request.user)

        if request.method == 'DELETE':
            return self.delete_from(Basket,
                                    self.kwargs.get('pk'), request.user)

    def add_in(self, model, recipe_id, user):
        if model.objects.filter(user=user, recipe__id=recipe_id):
            return Response({'error': 'Такой рецепт уже есть в корзине!'})
        recipe = get_object_or_404(Recipe, id=recipe_id)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipesSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, recipe_id, user):
        basket = model.objects.filter(user=user, recipe__id=recipe_id)
        if not basket.exists():
            return Response({'error': 'Данный рецепт уже удален из корзины.'},
                            status=status.HTTP_400_BAD_REQUEST)
        basket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        user = request.user

        if not Basket.objects.filter(user=user).exists():
            return Response({'error': 'В корзине ничего нет!'},
                            status=status.HTTP_400_BAD_REQUEST)

        ingredients = IngredientsRecipes.objects.filter(
            recipe__basket__user=user
        )
        ingredients_value = ingredients.values(
            'ingredient__name',
            'ingredient__measurement_unit',
        ).annotate(amount=Sum('amount'))

        first_string = (
            f'Пользователь {user.get_full_name()} \n\n'
        )
        shoping_list = '\n'.join([f'{ing["ingredient__name"]} '
                                  f'{ing["amount"]} '
                                  f'{ing["ingredient__measurement_unit"]}'
                                  for ing in ingredients_value])
        footer = '\n\n\nFoodgram project'

        ready_list = first_string + shoping_list + footer
        filename = f'{user.username}_shopping_list.txt'
        response = HttpResponse(ready_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
