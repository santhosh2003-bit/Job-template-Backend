from flask import Flask
import logging
import os
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
dotenv_path = os.path.join(parent_dir, ".env")
load_dotenv(dotenv_path)
# log_level = os.environ.get("LOG_LEVEL", "INFO")
# log_path = os.environ.get()

app = Flask(__name__, static_folder="static")
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

# Import your models here so that they are registered with SQLAlchemy.
from app.db.userauthmodel import User

with app.app_context():
    db.create_all()
