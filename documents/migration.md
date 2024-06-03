### migration
'''
はじめにやること、マイグレーションとスーパーユーザーの作成。
'''

python3 -m venv venv
pip install -r requirements.txt

setting
PYTHONUNBUFFERED=1;DJANGO_SETTINGS_MODULE=django_rest_sns.settings

'''
dockerに接続して、
docker exec -it postgres_container_sns bash
DBとの接続する。
$ psql -U admin -d postgres_db_sns
スキーマを作る。

CREATE SCHEMA postgre_db_sns;
\q クイットする。
'''
python manage.py makemigrations

python manage.py migrate

# create super user
python manage.py createsuperuser

# run server
python manage.py runserver localhost:8001

# ------------------------------------------
# テストの実施方法
# ------------------------------------------
# run test
python manage.py test

# ------------------------------------------
# テスト・データの作成方法
# ------------------------------------------
# Fixture
python manage.py loaddata api/init_data/custom_users.json

python manage.py loaddata sns_app/init_data/profiles.json

# ------------------------------------------
# ライブラリーの一括インストール方法。
# ------------------------------------------
# requests.txt 一括インストール。
$ pip install -r requirements.txt
# パッケージをインストールしたら、requirements.txtを更新する。

# ------------------------------------------
# アプリの登録、作成方法。
# ------------------------------------------
$ python manage.py startapp command_batch

$ python manage.py startapp sns_app
$ python manage.py startapp api
$ python manage.py startapp api_v1
$ python manage.py startapp api_v2 etc.........

