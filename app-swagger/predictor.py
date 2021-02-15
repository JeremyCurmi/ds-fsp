import os
import sys
import pickle
import flasgger
from flasgger import Swagger
from flask import Flask, request

app=Flask(__name__) # from which point you want to start the app
Swagger(app)

@app.route('/') # decorater # this is my route api
def welcome():
    return "Welcome All"

print("loading model ...")
model_path = f"models/model.pkl"
model = pickle.load(open(model_path, 'rb'))
ml_features_list = ["DiffPts","HTHG","B365H","B365D","HTLossStreak3","HTR_H","HTP","DiffFormPts","ATFormPts"]
 
@app.route('/predict', methods=["GET"]) # when method is not specified, automatically its set as GET
def predict_instance():
    """
     Let's Classify Football Score
    ---
    parameters:
        - name: DiffPts
          in: query
          type: number
          required: true
        - name: HTHG
          in: query
          type: number
          required: true
        - name: B365H
          in: query
          type: number
          required: true
        - name: B365D
          in: query
          type: number
          required: true
        - name: HTLossStreak3
          in: query
          type: number
          required: true
        - name: HTR_H
          in: query
          type: number
          required: true
        - name: HTP
          in: query
          type: number
          required: true
        - name: DiffFormPts
          in: query
          type: number
          required: true
        - name: ATFormPts
          in: query
          type: number
          required: true
    responses:
        200:
            description: The output values    
    """
    ml_features = []
    for i,feature in enumerate(ml_features_list):
        ml_features.append(float(request.args.get(feature)))
    prediction = model.predict([ml_features])
    return f"The predicted value is {prediction}"
    
@app.route("/predict_proba", methods=["GET"]) # when method is not specified, automatically its set as GET
def predict_proba_instance():
    """
     Let's Classify Football Score
    ---
    parameters:
        - name: DiffPts
          in: query
          type: number
          required: true
        - name: HTHG
          in: query
          type: number
          required: true
        - name: B365H
          in: query
          type: number
          required: true
        - name: B365D
          in: query
          type: number
          required: true
        - name: HTLossStreak3
          in: query
          type: number
          required: true
        - name: HTR_H
          in: query
          type: number
          required: true
        - name: HTP
          in: query
          type: number
          required: true
        - name: DiffFormPts
          in: query
          type: number
          required: true
        - name: ATFormPts
          in: query
          type: number
          required: true
    responses:
        200:
            description: The output values
    """
    ml_features = []
    for i,feature in enumerate(ml_features_list):
        ml_features.append(float(request.args.get(feature)))
    prediction = model.predict_proba([ml_features])
    return f"The predicted probabilities for {model.classes_} are: {prediction}"   

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)