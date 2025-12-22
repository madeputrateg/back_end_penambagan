from database.db import db
from sqlalchemy_serializer import SerializerMixin


class feedback(db.Model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    age = db.Column(db.Integer, nullable=True)
    sex = db.Column(db.String(10), nullable=True)
    fbs = db.Column(db.String(50), nullable=True)
    restecg = db.Column(db.String(50), nullable=True)
    exang = db.Column(db.String(50), nullable=True)
    oldpeak = db.Column(db.Integer, nullable=True)
    cp = db.Column(db.String(50), nullable=True)
    chol = db.Column(db.Integer, nullable=True)
    slope = db.Column(db.String(50), nullable=True)
    ca = db.Column(db.Integer, nullable=True)

    thal = db.Column(db.String(50), nullable=True) 
    
    trestbps = db.Column(db.Integer, nullable=True)
    pred_target = db.Column(db.String(50), nullable=True)
    target = db.Column(db.String(50), nullable=True)
    valid = db.Column(db.Boolean)


class serializefeedback(db.Model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feature_id = db.Column(db.Integer, db.ForeignKey('modelfeatures.id'), nullable=False)
    value = db.Column(db.String(50))
    input_id = db.Column(db.String(50),db.ForeignKey('feedback_input_target.id',ondelete="CASCADE"))

