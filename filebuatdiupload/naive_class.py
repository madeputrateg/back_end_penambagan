import numpy as np
import pandas as pd

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