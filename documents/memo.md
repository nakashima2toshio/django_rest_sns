【データベース作成権限をDjangoユーザーへ付加する】
解決策は、

ユーザーへデータベースの作成権限を付加すること！

１. コンテナのbashに入る

- docker exec -it postgres_container bash

- $ psql -U postgres -d postgres_db_sns


２. Djangoで使用しているユーザーに権限を付加する

- ALTER ROLE admin CREATEDB;


- schema一覧
  \dn

- DB一覧の取得
  \l

- DBの作成
  create database postgres_db_todo;
