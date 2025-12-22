from database.db import db
from models.model_feature import modelFeature

class modelFeatureReposeitory():

    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance
    
    def get_model_feature(self,model_id):
        allFeature = modelFeature.query.filter_by(model_id=model_id).all()
        return allFeature

    def get_all_model_feature(self):
        return modelFeature.query.all()
    
    def insert_model_feature(self,model_id,feature_name,feature_type):
        new_feature = modelFeature(model_id = model_id,feature_name = feature_name,feature_type = feature_type)
        db.session.add(new_feature)
        db.session.commit()

    


RepositoryFeatureModelAPI = modelFeatureReposeitory()

    #     __tablename__ = 'modelfeatures'
    # __table_args__ = {'extend_existing': True}
    # id = db.Column(db.Integer, primary_key= True)
    # model_id = db.Column(db.Integer, db.ForeignKey('machinemodels.id'), nullable=False)
    # feature_name = db.Column(db.String(20))
    # feature_type = db.Column(db.String(20))