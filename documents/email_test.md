##### python manage.py runserver
| 機能                       | URL                                                          |
| -------------------------- | ------------------------------------------------------------ |
| 1. アカウント仮登録        | http://localhost:8000/api/auth/users/                        |
| - tokenの取得              | http://localhost:8000/api/auth/jwt/create/                   |
| 2. アカウント本登録        | http://localhost:8000/api/auth/users/activation/             |
| 3. アカウント本登録再送信  | http://localhost:8000/api/auth/users/resend_activation/      |
| 4. ログイン                | http://localhost:8000/api/auth/jwt/create/                   |
| 5. リフレッシュトークン    | http://localhost:8000/api/auth/jwt/refresh/                  |
| 6. 認証チェック            | http://localhost:8000/api/auth/jwt/verify/                   |
| 7. ユーザー情報取得        | http://localhost:8000/api/auth/users/me/                     |
| 8. ユーザー情報変更        | http://localhost:8000/api/auth/users/me/                     |
| 9. ユーザーリスト取得      | http://localhost:8000/api/auth/users/                        |
| 10. メールアドレス変更     | (Djoserのデフォルトでは提供されていない)                     |
| 11. メールアドレス変更確認 | (Djoserのデフォルトでは提供されていない)                     |
| 12. パスワード変更         | http://localhost:8000/api/auth/users/set_password/           |
| 13. パスワードリセット     | http://localhost:8000/api/auth/users/reset_password/         |
| 14. パスワードリセット確認 | http://localhost:8000/api/auth/users/reset_password_confirm/ |
| 15. アカウント削除         | http://localhost:8000/api/auth/users/{username}/             |
| 16. アカウント削除確認     | (Djoserのデフォルトでは提供されていない)                     |
   
1. アカウント仮登録        | http://localhost:8000/api/auth/users/
   post:
    メールアドレス
    ユーザー名
    Password
    # -----------------------------------
    HTTP 201 Created
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "email": "user02@email.com",
        "username": "user02",
        "id": 7
    }
# -----------------------------------
tokenの取得
http://localhost:8000/api/auth/jwt/create/
post:
    username
    password
# -----------------------------------
POST /api/auth/jwt/create/
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNjA4OTQ3OSwiaWF0IjoxNzE1OTE2Njc5LCJqdGkiOiJjMTU2OTA1ZjQwMzU0MDU0YjlmYjEyZjY0NGJlOGY5YSIsInVzZXJfaWQiOjExfQ.kRpyw27QoC5n6bKIY94lBbhZQZDUnkmrP5OyKV6tPrM",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE1OTIwMjc5LCJpYXQiOjE3MTU5MTY2NzksImp0aSI6IjRjZjlkMWVjOTkwNjRlN2Q4NjgzNjZjMDVjMGNjYjdmIiwidXNlcl9pZCI6MTF9.PSFohvRIhHq4MyGlmfGpHC9aLrnnLQO0Nwf5sKMgidU"
}
    # -----------------------------------
    2. アカウント本登録
    http://localhost:8000/api/auth/users/activation/



    'EMAIL': {
        # アカウント本登録
        'activation': 'accounts.email.ActivationEmail',
        メールは、accounts/email.py
        
		class ActivationEmail(EmailManager):
        メール文面
        accounts/templates/accounts/activation.html
        
        
        
        # --------------------------------------------------------
        # アカウント本登録完了
        'confirmation': 'accounts.email.ConfirmationEmail',
        
        class ConfirmationEmail(EmailManager):
        メール文面
		accounts/templates/accounts/confirmation.html
        
        # --------------------------------------------------------
        # パスワードリセット
        'password_reset': 'accounts.email.PasswordResetEmail',
        
        
        # --------------------------------------------------------
        # パスワードリセット完了
        'password_changed_confirmation': 'accounts.email.PasswordChangedConfirmationEmail',
        
        # --------------------------------------------------------
        # メールアドレスリセット
        'username_reset': 'accounts.email.UsernameResetEmail',
        
        
        
        # メールアドレスリセット完了
        'username_changed_confirmation': 'accounts.email.UsernameChangedConfirmationEmail',
    },
    
    