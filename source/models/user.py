from database.db import db
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

class Userauth(UserMixin,SerializerMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) # Increased size for Postgres hashes
    # role = db.Column(db.String(20), default='user')