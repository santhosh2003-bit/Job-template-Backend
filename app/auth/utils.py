from flask import current_app, render_template, url_for
from itsdangerous import URLSafeSerializer
from flask_mail import Message
from app.server import mail

def generate_confirmation_token(data):
    serializer = URLSafeSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(data, salt=current_app.config["SECURITY_PASSWORD_SALT"])


def confirm_token(token, expiration=3600):
    serializer = URLSafeSerializer(current_app.config["SECRET_KEY"])
    try:
        data = serializer.loads(
            token,
            salt=current_app.config["SECURITY_PASSWORD_SALT"],
            max_age=expiration
        )
    except Exception:
        return False
    return data


def send_confirmation_email(user_email, token):
    confirm_url = url_for("auth.confirm_email", token=token, _external=True)
    html = render_template("activate.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    msg = Message(subject, recipients=[user_email], html=html, sender=current_app.config['MAIL_DEFAULT_SENDER'])
    mail.send(msg)