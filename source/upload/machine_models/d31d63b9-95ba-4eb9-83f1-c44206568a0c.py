import numpy as np
import pandas as pd

class knn2():
    def __init__(self,x_train,y_train,k,mean,std,features,y_target,colHash):
        self.X_train = x_train
        self.Y_train = y_train
        self.k=k
        self.mean = mean
        self.std = std
        self.features = features
        self.y_target = y_target
        self.hasher = colHash
    def euclidean_distance(self,a, b):
        return np.sqrt(np.sum((a - b)**2))

    def predict_one(self,x):
        distances = np.sqrt(((self.X_train - x)**2).sum(axis=1))
        k_indices = distances.argsort()[:self.k]
        k_nearest_labels = self.Y_train[k_indices]
        counts = np.bincount(k_nearest_labels)
        return counts.argmax()
    
    def pred(self,dataJson):
        data = pd.DataFrame(dataJson)
        cat_cols = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope']
        for col in cat_cols:
            if col in data.keys():
                data[col] = data[col].map(self.hasher[col])
        data = data.reindex(columns=self.features)
        
        data = data.fillna(0.0)
        numpy_data = data.to_numpy()
        scaled = (numpy_data - self.mean) / self.std 
        predicted = self.predict_one(scaled)
        return self.y_target[int(predicted)]