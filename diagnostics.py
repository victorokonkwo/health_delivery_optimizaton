
"""
The module performs diagnostic tests related to the model, as well as the data
"""

import os
import sys
import json
import timeit
import pickle
import logging
import subprocess

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")

# Load config.json and get environment variables
with open('config.json', 'r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(config['output_folder_path'])
test_data_path = os.path.join(config['test_data_path'])
prod_deployment_path = os.path.join(config['prod_deployment_path'])
output_folder_path = os.path.join(config['output_folder_path'])

demo_data = pd.read_csv(os.path.join(output_folder_path, 'Patient_Demo.csv'))
visit_data = pd.read_csv(os.path.join(output_folder_path, 'Patient_Hospital_Visit.csv'))

# Function to get model predictions
def model_predictions(dir_path = test_data_path, file_path = 'test.csv'):

    # Load model
    with open(os.path.join(prod_deployment_path, "trainedmodel.pkl"), 'rb') as model:
        model = pickle.load(model)

    # Read data
    testdata = pd.read_csv(os.path.join(dir_path, file_path))
    col = ['lab_visit', 'clinic_visit', 'sex', 'visit_month', 'visit_day',
       'visit_type', 'hospital_visit', 'state']

    X_test = testdata[col]
    y_test = testdata['institution_visit_day']

    pred = model.predict(X_test.values)

    return pred, y_test


# Function to get missing data
def missing_data():

    nas = list(demo_data.isna().sum())
    napercents = [nas[i] / len(demo_data.index) for i in range(len(nas))]

    return napercents


# Function to get timings
def execution_time():

    timings = []
    scripts = ['training.py']
    for process in scripts:
        starttime = timeit.default_timer()
        os.system(f'python3 {process}')
        timing = timeit.default_timer() - starttime
        timings.append(timing)

    return timings


# Function to check dependencies
def outdated_packages_list():
    outdated = subprocess.check_output(
        ['pip', 'list', '--outdated']).decode(sys.stdout.encoding)

    return str(outdated)


if __name__ == '__main__':
    model_predictions()
    missing_data()
    execution_time()
    outdated_packages_list()
