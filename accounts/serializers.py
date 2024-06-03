# accounts/serializers.py
# accounts/serializers.py
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import UserAccount


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = UserAccount
        fields = ('id', 'email', 'username', 'password', 're_password')


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = UserAccount
        fields = ('id', 'email', 'username', 'is_active')
