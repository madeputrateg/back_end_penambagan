from database.db import db
from sqlalchemy.sql import func
import datetime


class session(db.Model):
    __tablename__ = 'sessions'
    id_user = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow) 
    # Updates time on every update
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow) 
    # Example using Server Side default (preferred for accuracy)
