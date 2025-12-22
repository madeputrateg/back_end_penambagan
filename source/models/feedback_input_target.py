from database.db import db
import uuid
from sqlalchemy_serializer import SerializerMixin

class feedback_input_target(db.Model,SerializerMixin):
    id = db.Column(db.String(50),primary_key = True,default = lambda: str(uuid.uuid4()))
    model_id = db.Column(db.Integer, db.ForeignKey('machinemodels.id'), nullable=False)
    target = db.Column(db.String(50))
    valid = db.Column(db.Boolean)
    pred_target = db.Column(db.String(50))