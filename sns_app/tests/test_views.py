# import pprint

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker

from api.models import CustomUser
from sns_app.models import Comment
from sns_app.models import Follow
from sns_app.models import Like
from sns_app.models import Post
from sns_app.models import Profile

fake = Faker()

class CustomUserViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username=fake.user_name(), password=fake.password())

    def test_authenticated_user_can_retrieve_their_own_user_info(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('customuser-detail', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_unauthenticated_user_cannot_retrieve_any_user_info(self):
        response = self.client.get(reverse('customuser-detail', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ProfileViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username=fake.user_name(), password=fake.password())
        self.profile = Profile.objects.create(custom_user=self.user, display_name=fake.name(), bio=fake.text())

    def test_authenticated_user_can_retrieve_own_profile_info(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('profile-detail', kwargs={'pk': self.profile.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['display_name'], self.profile.display_name)
        self.assertEqual(response.data['bio'], self.profile.bio)

    def test_unauthenticated_user_cannot_retrieve_profile_info(self):
        response = self.client.get(reverse('profile-detail', kwargs={'pk': self.profile.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_update_own_profile_info(self):
        self.client.force_authenticate(user=self.user)
        update_data = {'display_name': fake.name(), 'bio': fake.text()}
        response = self.client.patch(reverse('profile-detail', kwargs={'pk': self.profile.pk}), data=update_data)
        self.profile.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.profile.display_name, update_data['display_name'])
        self.assertEqual(self.profile.bio, update_data['bio'])

    def test_authenticated_user_can_delete_own_profile_info(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('profile-detail', kwargs={'pk': self.profile.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Profile.objects.filter(pk=self.profile.pk).exists())

    def test_unauthenticated_user_cannot_update_or_delete_profile_info(self):
        update_data = {'display_name': fake.name(), 'bio': fake.text()}
        response = self.client.patch(reverse('profile-detail', kwargs={'pk': self.profile.pk}), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(reverse('profile-detail', kwargs={'pk': self.profile.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PostViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username=fake.user_name(), password=fake.password())
        self.profile = Profile.objects.create(custom_user=self.user, display_name=fake.name(), bio=fake.text())
        self.post = Post.objects.create(author=self.profile, content=fake.text())  # 'custom_user' を削除

    def test_authenticated_user_can_create_post(self):
        self.client.force_authenticate(user=self.user)
        post_data = {'content': fake.text()}
        response = self.client.post(reverse('post-list'), data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], post_data['content'])
        self.assertEqual(response.data['profile'], self.profile.pk)

    def test_unauthenticated_user_cannot_create_post(self):
        post_data = {'content': fake.text()}
        response = self.client.post(reverse('post-list'), data=post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_retrieve_own_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], self.post.content)
        # self.assertEqual(response.data['profile'], self.profile.pk)
        self.assertEqual(response.data['author']['custom_user']['id'], self.profile.custom_user.pk)

    def test_unauthenticated_user_cannot_retrieve_post(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_update_own_post(self):
        self.client.force_authenticate(user=self.user)
        update_data = {'content': fake.text()}
        response = self.client.patch(reverse('post-detail', kwargs={'pk': self.post.pk}), data=update_data)
        self.post.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post.content, update_data['content'])

    def test_authenticated_user_can_delete_own_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_unauthenticated_user_cannot_update_or_delete_post(self):
        update_data = {'content': fake.text()}
        response = self.client.patch(reverse('post-detail', kwargs={'pk': self.post.pk}), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LikeViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='paul', password='password')
        self.profile = Profile.objects.create(custom_user=self.user, display_name='Paul Smith', bio='Hello')
        self.post = Post.objects.create(author=self.profile, content='Post-content')  # 'custom_user' を 'author' に変更
        self.like = Like.objects.create(custom_user=self.profile.custom_user, post=self.post)

    def test_authenticated_user_can_create_like(self):
        self.client.force_authenticate(user=self.user)
        like_data = {'post': self.post.pk, 'custom_user': self.user.pk}  # この行を修正
        response = self.client.post(reverse('like-list'), data=like_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['custom_user']['id'], self.user.pk)
        self.assertEqual(response.data['post'], self.post.pk)

    def test_unauthenticated_user_cannot_create_like(self):
        like_data = {'post': self.post.pk}
        response = self.client.post(reverse('like-list'), data=like_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_delete_own_like(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('like-detail', kwargs={'pk': self.like.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Like.objects.filter(pk=self.like.pk).exists())

    def test_unauthenticated_user_cannot_delete_like(self):
        response = self.client.delete(reverse('like-detail', kwargs={'pk': self.like.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class FollowViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='paul', password='password')
        self.profile = Profile.objects.create(custom_user=self.user, display_name='Paul Smith', bio='Hello!')

        self.user_to_follow = CustomUser.objects.create_user(username='john', password='password')
        self.profile_to_follow = Profile.objects.create(custom_user=self.user_to_follow, display_name='John Smith', bio='Hi!')

        self.follow = Follow.objects.create(follower=self.user, followed=self.user_to_follow)  # 修正箇所: 'following' -> 'followed'

    def test_authenticated_user_can_retrieve_own_follow(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('follow-detail', kwargs={'pk': self.follow.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['follower']['id'], self.user.pk)  # 'profile' を 'follower' に変更し、'id' を取得するように修正
        self.assertEqual(response.data['followed']['id'], self.user_to_follow.pk)  # 'id' を取得するように修正

    def test_unauthenticated_user_cannot_retrieve_follow(self):
        response = self.client.get(reverse('follow-detail', kwargs={'pk': self.follow.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_delete_own_follow(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('follow-detail', kwargs={'pk': self.follow.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Follow.objects.filter(pk=self.follow.pk).exists())

    def test_unauthenticated_user_cannot_delete_follow(self):
        response = self.client.delete(reverse('follow-detail', kwargs={'pk': self.follow.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class CommentViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='paul', password='password')
        self.profile = Profile.objects.create(custom_user=self.user, display_name='Paul Smith', bio='Hello i am paul')
        self.post = Post.objects.create(author=self.profile, content='This is a paul Post')
        self.comment = Comment.objects.create(custom_user=self.user, post=self.post, content='This Comment was Paul-content')

    def test_authenticated_user_can_create_comment(self):
        self.client.force_authenticate(user=self.user)
        comment_data = {'post': self.post.pk, 'content': fake.text()}
        response = self.client.post(reverse('comment-list'), data=comment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['custom_user']['id'], self.user.pk)  # この行を修正
        self.assertEqual(response.data['post'], self.post.pk)
        self.assertEqual(response.data['content'], comment_data['content'])

    def test_unauthenticated_user_cannot_create_comment(self):
        comment_data = {'post': self.post.pk, 'content': fake.text(), 'custom_user': self.user.pk}
        response = self.client.post(reverse('comment-list'), data=comment_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_retrieve_own_comment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('comment-detail', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['custom_user']['id'], self.user.pk)
        self.assertEqual(response.data['post'], self.post.pk)
        self.assertEqual(response.data['content'], self.comment.content)

    def test_unauthenticated_user_cannot_retrieve_comment(self):
        response = self.client.get(reverse('comment-detail', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_update_own_comment(self):
        self.client.force_authenticate(user=self.user)
        update_data = {'content': fake.text()}
        response = self.client.patch(reverse('comment-detail', kwargs={'pk': self.comment.pk}), data=update_data)
        self.comment.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.comment.content, update_data['content'])

    def test_authenticated_user_can_delete_own_comment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('comment-detail', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_unauthenticated_user_cannot_update_or_delete_comment(self):
        update_data = {'content': fake.text()}
        response = self.client.patch(reverse('comment-detail', kwargs={'pk': self.comment.pk}), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(reverse('comment-detail', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
