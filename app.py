import logging
import os
import pytz

from email_validator import EmailNotValidError, validate_email
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "秘密鍵"
app.logger.setLevel(logging.DEBUG)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
toolbar = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'
db = SQLAlchemy(app)
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

class PastContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))

mail = Mail(app)

@app.route("/contact")
def contact():
    # DBに登録されたデータをすべて取得する
    pastcontacts = PastContact.query.all()
    return render_template("contact.html",pastcontacts = pastcontacts)


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # form属性を使ってフォームの値を取得する
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        # 入力チェック
        is_valid = True

        if not username:
            flash("ユーザ名は必須です")
            is_valid = False

        if not email:
            flash("メールアドレスは必須です")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください")
            is_valid = False

        if not description:
            flash("問い合わせ内容は必須です")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        # メールを送る
        send_email(
            email,
            "問い合わせありがとうございました。",
            "contact_mail",
            username=username,
            description=description,
        )

        # PastContactのインスタンスを作成
        pastcontact = PastContact(username=username, description=description)
        db.session.add(pastcontact)
        db.session.commit()

        # 問い合わせ完了エンドポイントへリダイレクトする
        flash("問い合わせありがとうございました。")
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")


@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    # 引数idに一致するデータを取得する
    pastcontact = PastContact.query.get(id)
    db.session.delete(pastcontact)
    db.session.commit()
    return redirect("../contact")

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)
