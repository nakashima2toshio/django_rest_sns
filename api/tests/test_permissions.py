from django.test import TestCase
from rest_framework.test import APIRequestFactory
from api.permissions import IsOwnerOrReadOnly
from sns_app.models import CustomUser, Profile
from api.serializers import ProfileSerializer


class IsOwnerOrReadOnlyTests(TestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='testuser1', email='testuser1@example.com', password='testpassword1')
        self.user2 = CustomUser.objects.create_user(username='testuser2', email='testuser2@example.com', password='testpassword2')
        self.profile1 = Profile.objects.create(custom_user=self.user1, display_name='Test User1', bio="Test bio 1")
        self.profile2 = Profile.objects.create(custom_user=self.user2, display_name='Test User2', bio="Test bio 2")

        self.factory = APIRequestFactory()
        self.permission = IsOwnerOrReadOnly()

    def test_owner_permission(self):
        request = self.factory.get('/')
        request.user = self.user1
        serializer = ProfileSerializer(instance=self.profile1)

        has_permission = self.permission.has_object_permission(request, None, self.profile1)
        self.assertTrue(has_permission)

    def test_not_owner_permission(self):
        request = self.factory.post('/')
        request.user = self.user2
        serializer = ProfileSerializer(instance=self.profile1)

        has_permission = self.permission.has_object_permission(request, None, self.profile1)
        self.assertFalse(has_permission)

    def test_not_authenticated_permission(self):
        request = self.factory.post('/')
        request.user = None
        serializer = ProfileSerializer(instance=self.profile1)

        has_permission = self.permission.has_object_permission(request, None, self.profile1)
        self.assertFalse(has_permission)
