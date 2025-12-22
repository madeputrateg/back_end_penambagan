from models.model import machineModel as mlModel
from database.db import db
from repository.model_feature import modelFeatureReposeitory, RepositoryFeatureModelAPI
from repository.feedback import feedbackRepository
from repository.feedback_input_target import APIrepoFeedbackTarget

class modelRepository():

    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance
    
    
    def get_all_model(self)->list[mlModel]:
        return mlModel.query.all()

    def insert_new_model(self,file_location,name,features):
        new_models = mlModel(file_location = file_location,name = name)
        db.session.add(new_models)
        db.session.commit()
        id = new_models.id
        repo = modelFeatureReposeitory()
        for name,dtype in features:
            repo.insert_model_feature(id,name,dtype)
        return new_models
    
    def get_all_model_feature_and_feedback(self):
        models = self.get_all_model()
        features = RepositoryFeatureModelAPI.get_all_model_feature()
        feedbacks = feedbackRepository.get_all_serialized_feedback()
        target_inputs = APIrepoFeedbackTarget.get_feedback_target()
        modelmap = {}
        # feature_id_to_model_hash = {}
        input_id_to_model_hash = {}
        for model in models:
            temp = {}
            temp["name"] = model.name
            temp["feature"] = {}
            temp["feedback"] = {}
            modelmap[model.id] = temp
        for feature in features:
            modelmap[feature.model_id]["feature"][feature.id] = feature.feature_name
            # feature_id_to_model_hash[feature.id] = feature.model_id
        for target_input in target_inputs :
            input_id_to_model_hash[target_input.id] = target_input.model_id
            temp = modelmap[target_input.model_id]["feedback"]
            temp[target_input.id] = {
                    "property": target_input.to_dict()
                }
        for feedback in feedbacks :
            temp = modelmap[input_id_to_model_hash[feedback.input_id]]
            feature_hash = temp["feature"]
            feedback_hash = temp["feedback"][feedback.input_id]
            if not ("feature" in feedback_hash):
                feedback_hash["feature"] = {}
            feedback_hash["feature"][feature_hash[feedback.feature_id]] = feedback.value
        return modelmap


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