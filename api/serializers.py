"""
CustomUserViewSet と ProfileViewSet の２つの ViewSet クラスを作成しました。
これらの ViewSet クラスはそれぞれ、
CustomUser モデルと SnsProfile モデルに対応する API エンドポイントを提供します。

get_queryset メソッドをオーバーライドして、認証されたユーザーに対してのみ、
自分自身の情報やプロフィール情報にアクセスできるように制限しています。
これにより、他のユーザーの情報へのアクセスが制限されます。

"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from sns_app.models import Profile

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        ref_name = 'API_CustomUser'

class ProfileSerializer(serializers.ModelSerializer):
    custom_user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['custom_user', 'display_name', 'bio']
        ref_name = 'APIProfile'
