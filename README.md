#### 問い合わせフォーム　機能概要
ユーザー名、メールアドレス、問い合わせ内容を入力し、お問い合わせボタンを押下すると、

問い合わせ完了ページに遷移し、入力したメールアドレス宛に問い合わせを受け付けた旨のメールが送信される。

また、ユーザー名、メールアドレス、問い合わせ内容のチェック機能も実装しており、

未入力、メールアドレスの形式かどうかのチェック機能を実装している。

問い合わせした内容はデータベースに保存され、トップページの過去のお問い合わせ一覧に

ユーザー名、問い合わせ日時、問い合わせ内容が表示される。


#### 送信側のメールアドレスの設定について
送信側のメールアドレスはGmailで2段階認証を設定し、

アプリパスワードページ([https://security.google.com/settings/security/apppasswords](https://security.google.com/settings/security/apppasswords))で

パスワードを取得する必要がある。

Gmailのメールアドレスとパスワードは.envファイルのMAIL_USERNAME、MAIL_PASSWORD、

MAIL_DEFAULT_SENDERに設定する。


#### データベースの生成について
アプリ実行前にDBを作成する必要がある。

ターミナルのPythonの対話モードで、app.py内で定義したflask_sqlalchemyの

インスタンスであるdb変数をインポートする。

	from app import db

DBの作成は「db.create_all()」コマンドを実行する。

	db.create_all()

app.pyの同階層に拡張子.dbのファイルが生成される。
