#
""" [単体テスト→シナリオテスト]　メール連携のテストとなるので。
- 1. APIで、アカウント（ユーザ）（仮）登録（Post)
　　　「ユーザ本登録」Resメールに応答（メール内のURLで）（メール内の、uid, tokenを取得）、アクティベーション実施
　　　OKのリターンメールを確認

 -2. パスワードリセット、再登録。

 - 3. メールアドレスの変更、変更完了。

 -4. ログイン、ログアウトのテスト。

"""
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
signup_url = reverse("accounts:account_signup")
activation_url = reverse("accounts:account_activation_sent")
login_url = reverse("accounts:account_login")


class TokenObtainTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse(signup_url)       # create user: http://localhost:8000/api/auth/users/
        self.login_url = reverse('token_login')     # activate user: http://localhost:8000/api/auth/users/activation/

        self.signup_data = {
            "email": "test@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "name": "Test User"
        }

    def test_token_obtain(self):
        # ユーザーをサインアップ
        response = self.client.post(self.signup_url, self.signup_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['email'], self.signup_data['email'])

        # サインアップしたユーザーでログインしてトークンを取得
        login_data = {
            "email": self.signup_data['email'],
            "password": self.signup_data['password1']
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 200)

        # トークンが正しく取得できたことを確認
        token = response.data.get('access')
        self.assertIsNotNone(token)

        # トークンを使用して認証されたリクエストを行う（例：ユーザー情報の取得）
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('user:me'))  # 'user:me'はDjoserのユーザー情報取得エンドポイントのURL名です。適切なURL名に変更してください。
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], self.signup_data['email'])
        self.assertEqual(response.data['name'], self.signup_data['name'])

    def tearDown(self):
        # テストケースの実行後に作成したユーザーを削除
        User.objects.filter(email=self.signup_data['email']).delete()


class TestAccounts(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('user:register')  # 'user:register'はDjoserのユーザー登録エンドポイントのURL名です。適切なURL名に変更してください。
        self.login_url = reverse('token_login')  # 'token_login'はSimpleJWTのトークン取得エンドポイントのURL名です。適切なURL名に変更してください。

        self.signup_data = {
            "email": "test@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "name": "Test User"
        }

    def test_jwt_login(self):
        self.client = APIClient()
        self.client.post('api/auth/jwt/create/', {'title': 'new idea'}, format='json')
        self.client.post('/notes/', {'title': 'another idea'}, format='json')

    def test_users_list(self):
        api_url = 'http://localhost:8000/api/accounts/users'
        self.client = APIClient()
        headers = {'Authorization': 'Bearer ' + self.token}
        payload = {'title': 'new idea'}
        response = self.client.post('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserTestCase(TestCase):
    #
    def setUp(self):
        self.client = APIClient()
        self.signup_data = {
            "email": "test@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "name": "Test User"
        }

    # 1. アカウント（仮）登録(signupペ ージでユーザーを作成
    def test_signup(self):
        response = self.client.post(signup_url, self.signup_data)
        self.assertEqual(response.status_code, 201)  # 仮登録が成功した場合のステータスコードを確認してください
        self.assertEqual(User.objects.count(), 1)

        # ユーザーがきちんと作らているか？
        # self.user = User.objects.first()
        # self.assertEqual(self.user.email, self.signup_data['email'])
        # self.assertEqual(self.user.name, self.signup_data['name'])
        # self.assertFalse(self.user.is_active)  # 仮登録後はユーザーは非アクティブ状態であるべきです
        #
        # # トークンの検証
        # token = response.data.get('token')
        # self.assertIsNotNone(token)
        #
        # refresh = RefreshToken(token)
        # self.assertEqual(str(refresh.access_token), token)
        #
        # # トークンの有効期限を確認
        # self.assertFalse(refresh.access_token.expired())

    # ユーザーがきちんと作らているか？
    def test_single_user(self):
        counter = User.objects.count()
        self.assertEqual(counter, 1)

        self.user = User.objects.first()
        self.assertEqual(self.user.name, self.signup_data['name'])
        self.assertEqual(self.user.email, self.signup_data['email'])

    # メールアドレスがverifiedになっているか？
    def test_email_address_verified(self):
        self.assertEqual(self.user.email.verified, True)

    # ログインページでのpostが正しく動作するか
    def test_login_page(self):
        data = {"email": self.user.email, "password": self.user.password}
        response = self.client.post(login_url, data)
        self.assertEqual(response.status_code, 200)

    # ログアウトの際にログインページへリダイレクトされているか？
    def test_logout(self):
        response = self.client.get("/accounts/logout/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, login_url)

    # verifiedされているユーザーの場合はきちんとログインできているか？
    def test_verified_user_login(self):
        self.client = APIClient()
        res_bool = self.client.login(email=self.user.email, password=self.user.password)
        self.assertEqual(res_bool, True)

    # verifiedされていないユーザーの場合はログインできない？
    def test_not_verified_user_login(self):
        response = self.client.post(signup_url, {"email": "not-verifed@itc.tokyo", "password1": "somepassword",
                                                 "password2": "somepassword"})
        self.assertEqual(response.status_code, 302)
        c = APIClient()
        res_bool = c.login(email="not-verified@itc.tokyo", password="somepassword")
        self.assertEqual(res_bool, False)

    def tearDown(self):
        # テストケースの実行後に作成したユーザーを削除
        User.objects.filter(email=self.signup_data['email']).delete()
