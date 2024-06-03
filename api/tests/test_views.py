#
"""
api/tests/test_views.py のユニットテスト要件。。

CustomUserViewSet テスト:
a. 認証済みユーザーが自分のユーザー情報を取得できること
b. 認証されていないユーザーがユーザー情報を取得できないこと
c. 認証済みユーザーが自分のユーザー情報を更新できること
d. 認証済みユーザーが自分のユーザー情報を削除できること
e. 認証されていないユーザーがユーザー情報を更新・削除できないこと

ProfileViewSet テスト:
a. 認証済みユーザーが自分のプロフィール情報を取得できること
b. 認証されていないユーザーがプロフィール情報を取得できないこと
c. 認証済みユーザーが自分のプロフィール情報を更新できること
d. 認証済みユーザーが自分のプロフィール情報を削除できること
e. 認証されていないユーザーがプロフィール情報を更新・削除できないこと
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import CustomUser
from sns_app.models import Profile, Post

class CustomUserViewSetTests(APITestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='testuser1', password='testpassword1')
        self.profile1 = Profile.objects.create(custom_user=self.user1, display_name='Test User1', bio='User1 bio')
        self.user2 = CustomUser.objects.create_user(username='testuser2', password='testpassword2')
        self.profile2 = Profile.objects.create(custom_user=self.user2, display_name='Test User2', bio='User2 bio')

        self.post = Post.objects.create(custom_user=self.user1, content='Sample post')

    def test_get_user_list_not_authenticated(self):
        url = reverse('customuser-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_list_authenticated(self):
        url = reverse('customuser-list')
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_detail_not_authenticated(self):
        url = reverse('customuser-detail', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_detail_authenticated(self):
        url = reverse('customuser-detail', args=[self.user1.id])
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ProfileViewSetTests(APITestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='testuser1', password='testpassword1')
        self.profile1 = Profile.objects.create(custom_user=self.user1, display_name='Test User1', bio='User1 bio')
        self.user2 = CustomUser.objects.create_user(username='testuser2', password='testpassword2')
        self.profile2 = Profile.objects.create(custom_user=self.user2, display_name='Test User2', bio='User2 bio')

        self.post = Post.objects.create(custom_user=self.user1, content='Sample post')

    def test_get_profile_list_not_authenticated(self):
        url = reverse('profile-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_list_authenticated(self):
        url = reverse('profile-list')
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile_detail_not_authenticated(self):
        url = reverse('profile-detail', args=[self.profile1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_detail_authenticated(self):
        url = reverse('profile-detail', args=[self.profile1.id])
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

