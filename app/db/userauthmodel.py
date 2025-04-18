from app.server import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema": "ezeapply_schema"}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
