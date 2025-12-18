from database.db import db

class machineModel(db.Model):
    __tablename__ = 'machinemodels'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    file_location = db.Column(db.String(70))
    name = db.Column(db.String(50))