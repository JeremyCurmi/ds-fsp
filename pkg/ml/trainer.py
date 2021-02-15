import pickle
from sklearn import ensemble
model = ensemble.RandomForestClassifier()

def train_model(model, X, y):
    return model.fit(X,y)

def save_model(model,
               model_path: str):
    pickle.dump(model, open(model_path, 'wb'))