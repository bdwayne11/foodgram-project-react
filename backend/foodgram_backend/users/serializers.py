# from rest_framework import serializers
# from djoser.serializers import UserSerializer
#
# from .models import CustomUser, Subscribe
# from api.serializers import ShortRecipesSerializer


# class GetUserSerializer(UserSerializer):
#     is_subscribed = serializers.SerializerMethodField()
#
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'id', 'username',
#                  'first_name', 'last_name',
#                  'is_subscribed')
#
#     def get_is_subscribed(self, obj):
#         user = self.context.get('request').user
#         if user.is_authenticated:
#             return Subscribe.objects.filter(user=user, author=obj.id).exists()
#         return False
#
#
# class SubscribeSerializer(GetUserSerializer):
#     recipes = ShortRecipesSerializer(many=True)
#     recipes_count = serializers.SerializerMethodField()
#
#     class Meta(GetUserSerializer.Meta):
#         fields = GetUserSerializer.Meta.fields + (
#             'recipes', 'recipes_count'
#         )
#
#     def get_recipes_count(self, obj):
#         return obj.recipes.count()


