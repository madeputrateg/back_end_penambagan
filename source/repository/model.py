from models.model import machineModel as mlModel
from database.db import db
from repository.model_feature import modelFeatureReposeitory

class modelRepository():

    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance
    
    
    def get_all_model(self):
        return mlModel.query.all()

    def insert_new_model(self,file_location,name,features):
        new_models = mlModel(file_location = file_location,name = name)
        db.session.add(new_models)
        db.session.commit()
        id = new_models.id
        repo = modelFeatureReposeitory()
        for name,dtype in features:
            repo.insert_model_feature(id,name,dtype)
        # return new_models
    
    def get_all_model_and_feature(self):
        repo = modelFeatureReposeitory()
        rawResult = mlModel.query.all()
        results = {}
        for model in rawResult:
            features = repo.get_model_feature(model.id)  
            data = {
                "model" : model,
                "features" : features
            }
            results[model.name] = data
            
        return results
    # __tablename__ = 'models'
    # __table_args__ = {'extend_existing': True}
    # id = db.Column(db.Integer, primary_key=True)
    # file_location = db.Column(db.String(70))
    # name = db.Column(db.String(50))