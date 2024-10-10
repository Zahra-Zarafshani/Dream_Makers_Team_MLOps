import numpy as np
import pandas as pd
import pickle

class Features:
        numerical_features =['diagnosis','radius_mean'
        'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean', 'compactness_mean', 'concavity_mean',
        'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean', 'radius_se', 'texture_se', 
        'perimeter_se', 'area_se', 'smoothness_se', 'compactness_se', 'concavity_se', 'concave points_se', 
        'symmetry_se', 'ractal_dimension_se', 'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
        'smoothness_worst', 'compactness_worst', 'concave points_worst', 'fractal_dimension_worst' ]
        file_features = []
        


class PredictionModel(Features):
    
    def __init__(self , input_object) : 
        self.features_value = [input_object[k] for k in Features.numerical_features]
        # file object can be added for further developments
        self. model = pickle.load(open('model.pkl', 'rb'))

    def computed_predictions(self):
        df = pd.DataFrame(self.features_value, columns=self.all_features)
        output = self.model.predict(df)
        #May be the following code must br written:
        #output = self.model.predict(df)[0]
        if output == 4:
            res_val = "Breast cancer"
        else:
            res_val = "no Breast cancer"
        return({'res_val': res_val})
     