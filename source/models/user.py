from database.db import db
from flask_login import UserMixin

class Userauth(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) # Increased size for Postgres hashes
    role = db.Column(db.String(20), default='user')