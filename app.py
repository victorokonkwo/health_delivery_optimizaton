import os
import json
import pickle

import pandas as pd
import numpy as np
from flask import Flask, session, jsonify, request

from scoring import score_model
from diagnostics import model_predictions, missing_data, execution_time, outdated_packages_list



# Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'

with open('config.json', 'r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(config['output_folder_path'])
output_model_path = os.path.join(config['output_model_path'])


with open(os.path.join(output_model_path, 'trainedmodel.pkl'), "rb") as model:
    prediction_model = pickle.load(model)


# Prediction Endpoint
@app.route("/prediction", methods=['POST', 'OPTIONS'])
def predict():
    filepath = request.json.get('filepath')
    pred, y_test = model_predictions(file_path=filepath)
    return str(pred)


# Scoring Endpoint
@app.route("/scoring", methods=['GET', 'OPTIONS'])
def scoring():
    score = score_model()

    return str(score)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
