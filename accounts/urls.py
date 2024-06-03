# accounts/urls.py
# from django.urls import path, include
# from .views import UserList, ActivateAccount, UserCreate
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserCreateView

router = DefaultRouter()
router.register(r'users', UserCreateView)

urlpatterns = [
    path('', include(router.urls)),
    # path('users/', UserList.as_view(), name='account_signup'),
    # path('users/create/', UserCreate.as_view(), name='account_create'),  # 新しいエンドポイント
    # path('activate/<uid>/<token>', ActivateAccount.as_view()),
]

"""
| 機能                  | URL                                                   |
|-----------------------|-------------------------------------------------------|
| 1. アカウント仮登録   | http://localhost:8000/api/auth/users/                 |
|   - tokenの取得       | http://localhost:8000/api/auth/jwt/create/            |
| 2. アカウント本登録   | api/auth/users/activation/                            |
| 3. アカウント本登録再送信 | api/auth/users/resend_activation/                  |
| 4. ログイン           | api/auth/jwt/create/                                  |
| 5. リフレッシュトークン | api/auth/jwt/refresh/                               |
| 6. 認証チェック       | api/auth/jwt/verify/                                  |
| 7. ユーザー情報取得   | api/auth/users/me/                                    |
| 8. ユーザー情報変更   | api/auth/users/me/                                    |
| 9. ユーザーリスト取得 | api/auth/users/                                       |
| 10. メールアドレス変更 | (Djoserのデフォルトでは提供されていない)               |
| 11. メールアドレス変更確認 | (Djoserのデフォルトでは提供されていない)           |
| 12. パスワード変更     | api/auth/users/set_password/                          |
| 13. パスワードリセット | api/auth/users/reset_password/                        |
| 14. パスワードリセット確認 | api/auth/users/reset_password_confirm/            |
| 15. アカウント削除     | api/auth/users/{username}/                            |
| 16. アカウント削除確認 | (Djoserのデフォルトでは提供されていない)               |

api/auth/ ^users/$ [name='useraccount-list']
api/auth/ ^users\.(?P<format>[a-z0-9]+)/?$ [name='useraccount-list']
api/auth/ ^users/activation/$ [name='useraccount-activation']     ## {uid: uid, token:token}
api/auth/ ^users/activation\.(?P<format>[a-z0-9]+)/?$ [name='useraccount-activation']
api/auth/ ^users/me/$ [name='useraccount-me']
api/auth/ ^users/me\.(?P<format>[a-z0-9]+)/?$ [name='useraccount-me']
api/auth/ ^users/resend_activation/$ [name='useraccount-resend-activation']
api/auth/ ^users/resend_activation\.(?P<format>[a-z0-9]+)/?$ [name='useraccount-resend-activation']
api/auth/ ^users/reset_password/$ [name='useraccount-reset-password']
api/auth/ ^users/reset_password\.(?P<format>[a-z0-9]+)/?$ [name='useraccount-reset-password']
api/auth/ ^users/reset_password_confirm/$ [name='useraccount-reset-password-confirm']
api/auth/ ^users/reset_password_confirm\.(?P<format>[a-z0-9]+)/?$ [name='useraccount-reset-password-confirm']
api/auth/ ^users/reset_username/$ [name='useraccount-reset-username']
api/auth/ ^users/reset_username\.(?P<format>[a-z0-9]+)/?$ [name='useraccount-reset-username']
api/auth/ ^users/reset_username_confirm/$ [name='useraccount-reset-username-confirm']
api/auth/ ^users/reset_username_confirm\.(?P<format>[a-z0-9]+)/?$ [name='useraccount-reset-username-confirm']
api/auth/ ^users/set_password/$ [name='useraccount-set-password']
api/auth/ ^users/set_password\.(?P<format>[a-z0-9]+)/?$ [name='useraccount-set-password']
api/auth/ ^users/set_username/$ [name='useraccount-set-username']
api/auth/ ^users/set_username\.(?P<format>[a-z0-9]+)/?$ [name='useraccount-set-username']
api/auth/ ^users/(?P<username>[^/.]+)/$ [name='useraccount-detail']
api/auth/ ^users/(?P<username>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='useraccount-detail']
api/auth/ ^$ [name='api-root']
api/auth/ ^\.(?P<format>[a-z0-9]+)/?$ [name='api-root']
api/auth/ ^jwt/create/? [name='jwt-create']
api/auth/ ^jwt/refresh/? [name='jwt-refresh']
api/auth/ ^jwt/verify/? [name='jwt-verify']
"""

""" djoser.urls
jwt_endpoints -----
（１）access tokenを取得する。有効期限は30分。
http://localhost:8000/api/v1/auth/jwt/create/
urlpatterns = [
    re_path(r"^jwt/create/?", views.TokenObtainPairView.as_view(), name="jwt-create"),
    re_path(r"^jwt/refresh/?", views.TokenRefreshView.as_view(), name="jwt-refresh"),
    re_path(r"^jwt/verify/?", views.TokenVerifyView.as_view(), name="jwt-verify"),
]
（２）

authtoken_endpoints -----
urlpatterns = [
    re_path(r"^token/login/?$", views.TokenCreateView.as_view(), name="login"),
    re_path(r"^token/logout/?$", views.TokenDestroyView.as_view(), name="logout"),
]

"""
