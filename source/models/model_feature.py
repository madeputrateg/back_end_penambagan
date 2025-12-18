from database.db import db

class modelFeature(db.Model):
    __tablename__ = 'modelfeatures'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key= True)
    model_id = db.Column(db.Integer, db.ForeignKey('machinemodels.id'), nullable=False)
    feature_name = db.Column(db.String(20))
    feature_type = db.Column(db.String(20))