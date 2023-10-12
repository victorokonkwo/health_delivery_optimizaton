"""
This module computes the scoring of the trained model
"""
import os
import json
import pickle
import logging

import pandas as pd
from sklearn import metrics

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")

# Load config.json and get path variables
with open('config.json', 'r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(config['output_folder_path'])
test_data_path = os.path.join(config['test_data_path'])
artifacts_path = os.path.join(config['output_model_path'])


# Function for model scoring
def score_model():

    with open(os.path.join(artifacts_path, 'trainedmodel.pkl'), "rb") as file:
        model = pickle.load(file)

    testdata = pd.read_csv(os.path.join(test_data_path, 'test.csv')).reset_index()
    
    col = ['lab_visit', 'clinic_visit', 'sex', 'visit_month', 'visit_day',
       'visit_type', 'hospital_visit', 'state']
    X_test = testdata[col]
    y_test = testdata['institution_visit_day']

    pred = model.predict(X_test.values)
    print(pred)

    mse_score = metrics.mean_squared_error(pred, y_test)

    # Save metrics
    with open(os.path.join(artifacts_path, "latestscore.txt"), 'w') as file:
        file.write(str(mse_score))

    logging.info(f"Scoring: MSE={mse_score:.2f}")

    return mse_score

if __name__ == '__main__':
    score_model()
