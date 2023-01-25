from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import GetUserSerializer, SubscribeSerializer

from .models import CustomUser, Subscribe


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GetUserSerializer

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        user = request.user
        serializer = GetUserSerializer(
            user,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,),
        url_path='subscribe'
    )
    def subscribe(self, request, **kwargs):
        print(kwargs)
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(CustomUser, id=author_id)

        if request.method == 'POST':
            serializer = SubscribeSerializer(
                author,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            sub = get_object_or_404(Subscribe, user=user,
                                    author=author)
            sub.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='subscriptions'
    )
    def subscriptions(self, request):
        user = request.user
        queryset = CustomUser.objects.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
