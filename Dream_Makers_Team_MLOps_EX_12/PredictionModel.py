import numpy as np
import pandas as pd
import pickle

class Features:
        numerical_features =['age','sex','cp','trestbps','chol',
                             'fbs','restecg','thalach','exang',
                             'oldpeak','slope','ca','thal'
                            ]
        num_feature_description = {'age':'Age',
                    'sex':'Sex',
                    'cp':'Chest pain type (4 values)',
                    'trestbps':'Resting blood pressure',
                    'chol':'Serum cholestoral in mg/dl',
                    'fbs':'Fasting blood sugar mg/dl',
                    'restecg':'Resting electrocardiographic (values 0,1,2)',
                    'thalach':'Maximum heart rate achieved',
                    'exang':'condition Exercise induced angina',
                    'oldpeak':'ST depression induced by exercise relative to rest',
                    'slope':'The slope of the peak exercise ST segment',
                    'ca':'Number of major vessels (0-3) colored by flourosopy',
                    'thal':'thal: 0 = normal; 1 = fixed defect; 2 = reversable defect',
                    }
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
     