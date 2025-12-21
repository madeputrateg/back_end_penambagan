import uuid
from typing import Optional
from repository.model import modelRepository
import os
import pickle
import importlib
import importlib.util
import sys
import __main__

class modelStract():
    def __init__(self,model_path,class_name,model_pickle_path,features):
        self.model_path = model_path
        self.class_name = class_name
        self.model_pickle_path = model_pickle_path
        #name,type
        self.__features = features
    @property
    def features(self) -> list:
        return self.__features


class modelLoaded():
    def __init__(self,class_name,class_path,pkl_path,features):
        spec = importlib.util.spec_from_file_location(class_name, class_path)

        module = importlib.util.module_from_spec(spec)
        
        sys.modules[class_name] = module

        spec.loader.exec_module(module)

        self.features = features
        try:
            class_obj = getattr(module, class_name)
            setattr(__main__, class_name, class_obj)
        except AttributeError:
            print(f"Error: Class '{class_name}' not found in {class_path}")
        with open(pkl_path,'rb') as f:
            self.model = pickle.load(f)
    
    def predict(self,x:dict):
        inputDict = {}
        keys = x.keys()
        for name,data_type in self.features:
            if not (name in keys):
                print("error missing value")
                return "error"
            if data_type == "integer":
                inputDict[name] = int(x[name])
            else :
                inputDict[name] = x[name]
        try:
            return self.model.pred(inputDict)
        except :
            print("error running predict")
            return "error"


        

class modelSwapper():
    def __init__(self,save_route=""):
        self.model_mapper = {}
        self.model_loaded = {}
        self.route = save_route
        self.route_model = os.path.join(self.route,"machine_models")

        #load_existing_models
        
    
    def loadSavedModel(self):
        repo = modelRepository()
        dictOfAllModel = repo.get_all_model_and_feature()
        # dictOfAllModel = {"modelName":dictFeatureAndModel}
        #dictFeatureAndModel = {"model":model,"features":[modelFeature,modelFeature,modelFeature,...]} modelFeature maksudnya class nya
        for key in dictOfAllModel:
            file_loc = dictOfAllModel[key]["model"].file_location
            name = dictOfAllModel[key]["model"].name
            features = []
            for feature in dictOfAllModel[key]["features"]:
                features.append((feature.feature_name,feature.feature_type))
            python_path = os.path.join(self.route_model,file_loc + ".py")
            pkl_path = os.path.join(self.route_model,file_loc + ".pkl")
            self.model_loaded[name] = modelLoaded(name,python_path,pkl_path,features)
            self.model_mapper[name] = modelStract(python_path,name,pkl_path,features)
    
    def getModel(self,name) -> Optional[modelStract] :
        if name in self.model_mapper.keys():
            return self.model_mapper[name]
        else:
            print("model don't exist in the swapper map")

    def getModelKeys(self) :
        return self.model_mapper.keys()
    
    def getLoadedModel(self,name) -> Optional[modelLoaded]:
        if name in self.model_loaded.keys():
            return self.model_loaded[name]
        else:
            print("model don't exist in the swapper map")

    def getAllModelAndFeature(self):
        keys = self.getModelKeys()
        modelAndFeature = {}
        for modelName in keys:
            modelAndFeature[modelName] = self.model_mapper[modelName].features
        return modelAndFeature
    
    def initializedModel(self,class_name,features,pickle,class_model):
        #pickle_path
        uuid_unique =  uuid.uuid4().__str__()
        pickel_path = uuid_unique + ".pkl"
        class_path = uuid_unique + ".py"
        pickel_path = os.path.join(self.route_model,pickel_path)
        class_path = os.path.join(self.route_model,class_path)
        if class_name in self.model_mapper.keys():
            return "model existed"
        class_model.save(class_path)
        pickle.save(pickel_path)
        # modelRepository.Repository.insert_new_model(uuid_unique,class_name)
        model = modelRepository()
        model.insert_new_model(uuid_unique,class_name,features)
        self.model_loaded[class_name] = modelLoaded(class_name,class_path,pickel_path,features)
        self.model_mapper[class_name] = modelStract(class_path,class_name,pickel_path,features)
        return "success"

