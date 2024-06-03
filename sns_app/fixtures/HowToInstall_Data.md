#### sns_app以下に初期データを投入する順番は以下の通りです:

- Profile
- Post
- Like
- Comment
- Follow

##### データ投入コマンド


| データ投入コマンド                                                |
| ---------------------------------------------------------|
| python manage.py loaddata sns_app/fixtures/profiles.json |
| python manage.py loaddata sns_app/fixtures/post.json   |
| python manage.py loaddata sns_app/fixtures/like.json   |
| python manage.py loaddata sns_app/fixtures/comment.json   |
| python manage.py loaddata sns_app/fixtures/follow.json   |

##### データ投入の順番は、各テーブルが他のテーブルに依存する順番に従っています。

- Profileは他のテーブルに依存しないため、最初に投入されます。
- PostはProfile（正確にはCustomUser）に依存し、
- LikeとCommentはPostに依存しています。最後に、
- FollowはProfile（CustomUser）に依存しています。

- この順番でデータを投入することで、各テーブル間のリレーションが適切に設定されます。
- ただし、実際に初期データを投入する前に、
- apiのCustomUserの初期データを投入しておく必要があります。
- これは、ProfileがCustomUserに依存しているためです。
