#
"""
CustomUserSerializer のテスト

setUp メソッドで CustomUser インスタンスを作成し、シリアライザーに渡す。
テストメソッドでシリアライザーが期待通りに動作しているか検証する。
シリアライザーのデータに期待されるフィールドが含まれていることを確認する。
各フィールドの内容が正しいことを確認する。
ProfileSerializer のテスト

setUp メソッドで CustomUser インスタンスと Profile インスタンスを作成し、シリアライザーに渡す。
テストメソッドでシリアライザーが期待通りに動作しているか検証する。
シリアライザーのデータに期待されるフィールドが含まれていることを確認する。
各フィールドの内容が正しいことを確認する。
Profile シリアライザーの custom_user フィールドに関連する CustomUserSerializer が正しく動作していることを確認する。

"""
from django.test import TestCase
from api.serializers import CustomUserSerializer, ProfileSerializer
from django.contrib.auth import get_user_model
from sns_app.models import Profile

class CustomUserSerializerTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'id': 1,
            'username': 'paul',
            'email': 'paul@example.com',
            'first_name': 'Paul',
            'last_name': 'Smith',
        }
        self.user = get_user_model().objects.create(**self.user_data)

    def test_custom_user_serializer(self):
        serializer = CustomUserSerializer(instance=self.user)
        self.assertEqual(set(serializer.data.keys()), set(self.user_data.keys()))

        for key in self.user_data.keys():
            self.assertEqual(serializer.data[key], self.user_data[key])

class ProfileSerializerTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='paul', password='password')
        self.profile_data = {
            'custom_user': self.user,
            'display_name': 'Paul Smith',
            'bio': 'Software Developer',
        }
        self.profile = Profile.objects.create(**self.profile_data)

    def test_profile_serializer(self):
        serializer = ProfileSerializer(instance=self.profile)
        expected_keys = set(['custom_user', 'display_name', 'bio'])

        self.assertEqual(set(serializer.data.keys()), expected_keys)

        self.assertEqual(serializer.data['display_name'], self.profile_data['display_name'])
        self.assertEqual(serializer.data['bio'], self.profile_data['bio'])

        user_serializer = CustomUserSerializer(instance=self.user)
        self.assertEqual(serializer.data['custom_user'], user_serializer.data)

