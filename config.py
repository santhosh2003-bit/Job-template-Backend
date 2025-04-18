import os
import urllib.parse


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")
    USERNAME = os.environ.get("RDBMS_DB_USERNAME")
    PASSWORD = urllib.parse.quote(os.environ.get("RDBMS_DB_PASSWORD"))
    DB_NAME = os.environ.get("RDBMS_DB_NAME")
    HOSTNAME = os.environ.get("RDBMS_DB_HOSTNAME")
    DB_PORT = os.environ.get("RDBMS_DB_PORT")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", "my_precious_two")

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "rajputyash.0305@gmail.com"
    MAIL_PASSWORD = "oohl hbbq beny bses"
    MAIL_DEFAULT_SENDER = "rajputyash.0305@gmail.com"