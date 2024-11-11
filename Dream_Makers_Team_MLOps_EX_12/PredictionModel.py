import numpy as np
import pandas as pd
import pickle

class Features:
        numerical_features =['age','sex','cp','trestbps','chol',
                             'fbs','restecg','thalach','exang',
                             'oldpeak','slope','ca','thal','condition'
]
        file_features = []
        

class PredictionModel(Features):
    
    def __init__(self , input_object) : 
        self.features_value = [input_object[k] for k in Features.numerical_features]
        print("=============================")
        print(self.features_value)
        print("=============================")
        # file object can be added for further developments
        self. model = pickle.load(open('model.pkl', 'rb')) 

    def computed_predictions(self):
        output = self.model.predict([self.features_value])[0]
        if output == 4:
            res_val = "Breast Cancer"
        else:
            res_val = "No Breast Cancer"
        return({'cancer_stat': res_val})
     