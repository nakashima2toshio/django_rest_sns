from django.test import TestCase
from api.serializers import CustomUserSerializer
from sns_app.serializers import PostSerializer, LikeSerializer, CommentSerializer, FollowSerializer, ProfileSerializer
from api.models import CustomUser
from sns_app.models import Post, Like, Comment, Follow, Profile
from sns_app.tests.test_views import fake


class CustomUserSerializerTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'id': 1,
            'username': 'paul',
            'email': '',
            'first_name': '',
            'last_name': '',
        }
        self.user = CustomUser.objects.create(**self.user_data)

    def test_custom_user_serializer(self):
        serializer = CustomUserSerializer(instance=self.user)
        self.assertEqual(set(serializer.data.keys()), set(self.user_data.keys()))

        for key in self.user_data.keys():
            self.assertEqual(serializer.data[key], self.user_data[key])


class ProfileSerializerTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='paul', password='password')
        self.profile_data = {
            'custom_user': self.user,
            'display_name': 'Paul Smith',
            'bio': 'Software Developer',
        }
        self.profile = Profile.objects.create(**self.profile_data)

    def test_profile_serializer(self):
        serializer = ProfileSerializer(instance=self.profile)
        expected_keys = {'custom_user', 'display_name', 'bio'}

        self.assertEqual(set(serializer.data.keys()), expected_keys)

        self.assertEqual(serializer.data['display_name'], self.profile_data['display_name'])
        self.assertEqual(serializer.data['bio'], self.profile_data['bio'])

        user_serializer = CustomUserSerializer(instance=self.user)
        self.assertEqual(serializer.data['custom_user'], user_serializer.data)


class PostSerializerTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username=fake.user_name(), password=fake.password())
        self.profile = Profile.objects.create(custom_user=self.user, display_name=fake.name(), bio=fake.text())
        self.post = Post.objects.create(author=self.profile, content=fake.text())  # 'author' を使用

    def test_post_serializer(self):
        serializer = PostSerializer(instance=self.post)
        expected_keys = {'id', 'author', 'content', 'created_at'}
        self.assertEqual(set(serializer.data.keys()), expected_keys)
        self.assertEqual(serializer.data['content'], self.post.content)
        user_serializer = ProfileSerializer(instance=self.profile)
        self.assertEqual(serializer.data['author'], user_serializer.data)


class LikeSerializerTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='paul', password='password')
        self.profile = Profile.objects.create(custom_user=self.user, display_name='Paul Smith',
                                              bio='Software Developer')
        self.post = Post.objects.create(author=self.profile, content='This is a test post.')
        self.like = Like.objects.create(custom_user=self.user, post=self.post)

    def test_like_serializer(self):
        serializer = LikeSerializer(instance=self.like)
        expected_keys = {'id', 'custom_user', 'post', 'created_at'}

        self.assertEqual(set(serializer.data.keys()), expected_keys)

        user_serializer = CustomUserSerializer(instance=self.user)
        self.assertEqual(serializer.data['custom_user'], user_serializer.data)
        self.assertEqual(serializer.data['post'], self.post.id)


class CommentSerializerTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='paul', password='password')
        self.profile = Profile.objects.create(custom_user=self.user, display_name='Paul Smith',
                                              bio='Software Developer')
        self.post = Post.objects.create(author=self.profile, content='This is a test post.')
        self.comment_data = {
            'custom_user': self.user,
            'post': self.post,
            'content': 'This is a test comment.',
        }
        self.comment = Comment.objects.create(**self.comment_data)

    def test_comment_serializer(self):
        serializer = CommentSerializer(instance=self.comment)
        expected_keys = {'id', 'custom_user', 'post', 'content', 'created_at', 'updated_at'}

        self.assertEqual(set(serializer.data.keys()), expected_keys)

        self.assertEqual(serializer.data['content'], self.comment_data['content'])

        user_serializer = CustomUserSerializer(instance=self.user)
        self.assertEqual(serializer.data['custom_user'], user_serializer.data)
        self.assertEqual(serializer.data['post'], self.post.id)


class FollowSerializerTestCase(TestCase):
    def setUp(self):
        self.follower = CustomUser.objects.create_user(username='paul', password='password')
        self.followed = CustomUser.objects.create_user(username='john', password='password')
        self.follow = Follow.objects.create(follower=self.follower, followed=self.followed)

    def test_follow_serializer(self):
        serializer = FollowSerializer(instance=self.follow)
        expected_keys = {'id', 'follower', 'followed', 'timestamp'}

        self.assertEqual(set(serializer.data.keys()), expected_keys)

        follower_serializer = CustomUserSerializer(instance=self.follower)
        followed_serializer = CustomUserSerializer(instance=self.followed)
        self.assertEqual(serializer.data['follower'], follower_serializer.data)
        self.assertEqual(serializer.data['followed'], followed_serializer.data)
