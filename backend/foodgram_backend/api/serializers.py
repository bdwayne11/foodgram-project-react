import base64
import uuid

from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import F
from djoser.serializers import UserSerializer
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from recepts.models import (Basket, Favourites, Ingredients,
                            IngredientsRecipes, Recipe, Tag)
from users.models import CustomUser, Subscribe


class GetUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscribe.objects.filter(user=user, author=obj.id).exists()
        return False


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'


class CreateIngredientsRecipesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = IngredientsRecipes
        fields = ('id', 'amount')


# class IngredientsRecipesSerializer(serializers.ModelSerializer):
#     name = serializers.SlugRelatedField(
#         read_only=True,
#         source='ingredient',
#         slug_field='name'
#     )
#     measurement_unit = serializers.SlugRelatedField(
#         read_only=True,
#         source='ingredient',
#         slug_field='measurement_unit'
#     )
#
#     class Meta:
#         model = IngredientsRecipes
#         fields = (
#             'id',
#             'name',
#             'measurement_unit',
#             'amount'
#         )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    image = serializers.CharField(source="image.url")
    author = GetUserSerializer(read_only=True)
    # ingredients = IngredientsSerializer(read_only=True, many=True)
    # кажется, что это неправильно работает. amount?
    # ingredients = IngredientsRecipesSerializer(many=True, read_only=True)
    # это тоже не хочет работать...
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Favourites.objects.filter(user=user, recipe=obj.id).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Basket.objects.filter(user=user, recipe=obj.id).exists()
        return False

    def get_ingredients(self, obj):
        ingredients = obj.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('ingredientsrecipes__amount')
        )
        return ingredients


class ShortRecipesSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source="image.url")

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),
                               name=f'{uuid.uuid1()}.{ext}')

        return super().to_internal_value(data)


class WriteRecipesSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()
    ingredients = CreateIngredientsRecipesSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name',
                  'text', 'cooking_time')

    # Предполагаю, что сюда нужны транзацкии. Это так?

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        obj = [IngredientsRecipes(ingredient=Ingredients.objects.get(
            id=ing['id']
        ),
                                  recipe=recipe,
                                  amount=ing['amount'])
               for ing in ingredients]
        IngredientsRecipes.objects.bulk_create(obj)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        # instance = Recipe.objects.update(**validated_data)
        # почему это не работает????
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        IngredientsRecipes.objects.filter(recipe=instance).delete()
        IngredientsRecipes.objects.bulk_create([IngredientsRecipes(
            ingredient=Ingredients.objects.get(id=ing['id']),
            recipe=instance,
            amount=ing['amount']
        ) for ing in ingredients])

        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance,
                                context={'request':
                                         self.context.get('request')}).data


class SubscribeSerializer(GetUserSerializer):
    recipes = ShortRecipesSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta(GetUserSerializer.Meta):
        fields = GetUserSerializer.Meta.fields + (
            'recipes', 'recipes_count'
        )
        read_only_fields = ('email', 'username',
                            'first_name', 'last_name')

    def validate(self, attrs):
        author = self.instance
        user = self.context.get('request').user
        if Subscribe.objects.filter(author=author, user=user).exists():
            raise ValidationError(
                detail='Вы уже подписались на данного пользователя',
                code=status.HTTP_400_BAD_REQUEST
            )
        if author == user:
            raise ValidationError(
                detail='Нельзя подписаться на самого себя',
                code=status.HTTP_400_BAD_REQUEST
            )
        return attrs

    def get_recipes_count(self, obj):
        return obj.recipes.count()
