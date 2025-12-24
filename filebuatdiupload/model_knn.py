import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import os

df = pd.read_csv(r'C:\\Users\\putra\\OneDrive\Documents\\testerUpload\\heart.csv')

df.isnull().sum()
df.duplicated().sum()

df = df.drop(columns=['id', 'dataset'], errors='ignore')

num_cols = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
cat_cols = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope']

for col in num_cols:
    median_value = df[col].median()
    df[col].fillna(median_value, inplace=True)

for col in cat_cols:
    mode_value = df[col].mode()[0]
    df[col].fillna(mode_value, inplace=True)

df.isnull().sum()

drop_cols = ['id', 'dataset']
df = df.drop(columns=[c for c in drop_cols if c in df.columns])
print("Kolom setelah penghapusan kolom tidak relevan:")
print(df.columns.tolist())

colHash = {}
for col in cat_cols:
    unique_vals = df[col].unique()
    mapping = {val: idx for idx, val in enumerate(unique_vals)}
    colHash[col] = mapping
    df[col] = df[col].map(mapping)
    print("hasil encoding kategorikal (5 baris pertama):")
    print(df[cat_cols].head())

X = df[['sex', 'cp', 'thalach', 'exang',
        'oldpeak', 'slope', 'ca', 'thal']].values
y = df['target'].values

X_mean = X.mean(axis=0)
X_std = X.std(axis=0)
X_scaled = (X - X_mean) / X_std

np.random.seed(42)
indices = np.arange(len(X_scaled))
np.random.shuffle(indices)

split = int(0.8 * len(X_scaled))
train_idx, test_idx = indices[:split], indices[split:]

x_train, x_test = X_scaled[train_idx], X_scaled[test_idx]
y_train, y_test = y[train_idx], y[test_idx]




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



#save model
feature = ['sex', 'cp', 'thalach', 'exang',
        'oldpeak', 'slope', 'ca', 'thal']
y_target = ["no disease","disease"]
model_knn = knn2(x_train,y_train,5,X_mean,X_std,feature,y_target,colHash)
knn_path = r"C:\Users\putra\OneDrive\Documents\testerUpload\ModelKnnNaiveBayesJantung\knn.pkl"
with open(knn_path,"wb") as f:
    pickle.dump(model_knn,f)
data = [
    # {
    #     "age": 52, "sex": 1, "cp": 0, "trestbps": 125, "chol": 212, 
    #     "fbs": 0, "restecg": "test", "thalach": 168, "exang": 0, 
    #     "oldpeak": 1, "slope": 2, "ca": 2, "thal": 3, "target": 0
    # }
    {
        "age": 52, "sex": 1, "cp": 0, "trestbps": 125, "chol": 212, 
         "restecg": "test", "thalach": 168, "exang": 0, 
        "oldpeak": 1, "slope": 2, "ca": 2, "thal": 3, "target": 0
    }
]

print(model_knn.pred(data))

class navie_baise():
    def __init__(self, x, y, feature, mean, std, y_target,colHash):
        self.params = self.fit_gaussian_nb(x, y) # Added self.
        self.feature = feature
        self.mean = mean
        self.std = std
        self.y_target = y_target
        self.hasher = colHash

    def fit_gaussian_nb(self, X, y): # Added self
        classes = np.unique(y)
        params = {}
        for c in classes:
            X_c = X[y == c]
            params[c] = {
                "prior": X_c.shape[0] / X.shape[0],
                "mean": X_c.mean(axis=0),
                "var": X_c.var(axis=0) + 1e-9
            }
        return params

    def predict_gaussian_nb(self, X):
        # ... (your existing logic is fine here) ...
        # Ensure it returns a single value if only one row is passed
        classes = list(self.params.keys())
        n_samples = X.shape[0]
        log_posteriors = np.zeros((n_samples, len(classes)))

        for idx, c in enumerate(classes):
            prior = self.params[c]["prior"]
            mean = self.params[c]["mean"]
            var = self.params[c]["var"]

            # log-likelihood Gaussian per sample
            # rumus: -0.5*sum(log(2πσ²)) - 0.5*sum((x-μ)²/σ²)
            log_likelihood = -0.5 * np.sum(np.log(2 * np.pi * var))
            log_likelihood -= 0.5 * np.sum(((X - mean) ** 2) / var, axis=1)

            log_posteriors[:, idx] = np.log(prior) + log_likelihood
        class_indices = np.argmax(log_posteriors, axis=1)
        return class_indices 

    def pred(self, dataJson):
        data = pd.DataFrame(dataJson)
        
        data = data.reindex(columns=self.feature) # Changed to self.feature
        cat_cols = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope']
        for col in cat_cols:
            if col in data.keys():
                data[col] = data[col].map(self.hasher[col])
        data = data.reindex(columns=self.features)
        
        data = data.fillna(0.0)
        numpy_data = data.to_numpy()
        
        # Scaling
        scaled = (numpy_data - self.mean) / self.std 
        
        # Call the correct prediction method
        predicted_idx = self.predict_gaussian_nb(scaled)
        return predicted_idx


model_naive = navie_baise(x_train,y_train,feature,X_mean,X_std,y_target,colHash)
naive_path = r"C:\Users\putra\OneDrive\Documents\testerUpload\ModelKnnNaiveBayesJantung\naive.pkl"
with open(naive_path,"wb") as f:
    pickle.dump(model_naive,f)
# gnb_params = fit_gaussian_nb(x_train, y_train)
