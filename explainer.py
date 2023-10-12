import os
import json
import pickle

import pandas as pd

from flask import Flask
from explainerdashboard import RegressionExplainer, ExplainerDashboard


app = Flask(__name__)

with open('config.json', 'r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(config['output_folder_path'])
test_data_path = os.path.join(config['test_data_path'])
artifacts_path = os.path.join(config['output_model_path'])

with open(os.path.join(artifacts_path, 'trainedmodel.pkl'), "rb") as file:
    model_xgb = pickle.load(file)

testdata = pd.read_csv(os.path.join(test_data_path, 'test.csv')).reset_index()

col = ['lab_visit', 'clinic_visit', 'sex', 'visit_month', 'visit_day',
       'visit_type', 'hospital_visit', 'state']

X_test = testdata[col]
y_test = testdata['institution_visit_day']

explainer = RegressionExplainer(model_xgb, X_test, y_test)
db = ExplainerDashboard(explainer, server=app, url_base_pathname="/dashboard/", shap_interaction=False)

@app.route('/dashboard')
def return_dashboard():
    return db.app.index()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8051, threaded=True)
