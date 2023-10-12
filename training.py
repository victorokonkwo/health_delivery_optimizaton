"""
The module trains the Linear Regression Model
"""

import os
import json
import pickle
import logging

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")

# Load config.json and get path variables
with open('config.json', 'r') as f:
    config = json.load(f)



dataset_csv_path = os.path.join(config['output_folder_path'])
model_path = os.path.join(config['output_model_path'])

def preprocessing():
    """
    Preprocesses the data
    """

    df = os.path.join(dataset_csv_path, "Patient_Hospital_Visit.csv")
    df2 = os.path.join(dataset_csv_path, "Patient_Demo.csv")

    pat_visit = pd.read_csv(df)
    pat_demo = pd.read_csv(df2)

    demo_visit_df = pat_visit.merge(pat_demo, on=['patient_id', 'institution_id'], how='left')
    new_data = demo_visit_df.drop(['admitted_at', 'discharged_at','dob', 'visit_id', 'patient_id', 'inserted_at', 'institution_id', 'updated_at'], axis=1)

    demo_visit_df['dob'] = pd.to_datetime(demo_visit_df['dob'])
    demo_visit_df['inserted_at'] = pd.to_datetime(demo_visit_df['inserted_at'])

    demo_visit_df['age'] = np.floor((demo_visit_df['inserted_at'] - demo_visit_df['dob']).dt.days/365).fillna(0).astype(int)
    demo_visit_df['age_bin'] = pd.cut(demo_visit_df['age'], 4, labels=['Children/Teens', 'Adult', 'older adult', 'senior citizen'])

    demo_visit_df['visit_month'] = demo_visit_df['inserted_at'].dt.month
    demo_visit_df['visit_day'] = demo_visit_df['inserted_at'].dt.day

    ## The number of times a patient has visited a hospital, clinic, lab within a month

    no_of_visit = demo_visit_df.groupby(['patient_id', 'inserted_at', 'type'])['type'].count().unstack().fillna(0).rename(columns={'clinic':'clinic_visit','hospital':'hospital_visit', 'laboratory':'lab_visit'})
    no_of_visit = no_of_visit.reset_index()
    demo_visit_df = demo_visit_df.merge(no_of_visit, on=['patient_id', 'inserted_at'], how='left')
    institution_visit = demo_visit_df.groupby(['inserted_at', 'institution_id'])['visit_id'].count().reset_index().rename(columns={'visit_id':'institution_visit_day'})
    
    # Total number of patients admitted to the hospital in a day.
    demo_visit_df = demo_visit_df.merge(institution_visit, on=['inserted_at', 'institution_id'], how='left')

    train_df = demo_visit_df[demo_visit_df['inserted_at'].astype('str') <= '2021-06-31']
    test_df = demo_visit_df[demo_visit_df['inserted_at'].astype('str') > '2021-06-31']
    
    train_df = train_df.drop(['admitted_at', 'discharged_at','dob', 'visit_id', 'patient_id', 'inserted_at', 'institution_id', 'updated_at'], axis=1)
    test_df = test_df.drop(['admitted_at', 'discharged_at','dob', 'visit_id', 'patient_id', 'inserted_at', 'institution_id', 'updated_at'], axis=1)
    
    cat_col = ['visit_type', 'type', 'state', 'sex']
    num_col = ['visit_month', 'visit_day', 'clinic_visit', 'hospital_visit', 'lab_visit', 'institution_visit_day', 'age']

    # new_data = new_data.drop_duplicates()
    train_df = train_df.drop_duplicates()
    test_df = test_df.drop_duplicates()

    for col in cat_col:
        label_encoder = LabelEncoder()
        demo_visit_df[col] = label_encoder.fit_transform(demo_visit_df[col])
        train_df[col] = label_encoder.fit_transform(train_df[col])
        test_df[col] = label_encoder.fit_transform(test_df[col])

    #print(demo_visit_df.head())
    X = demo_visit_df[['lab_visit', 'clinic_visit', 'sex', 'visit_month', 'visit_day',
       'visit_type', 'hospital_visit', 'state']]
    y = demo_visit_df['institution_visit_day']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    test_path = os.path.join(dataset_csv_path, "test.csv")

    test_df.to_csv(test_path, index=False)
    return X_train, X_test, y_train, y_test
    

def train_model():

    # use this xgboost regression for training
    X_train, X_test, y_train, y_test = preprocessing()
    model_xgb = XGBRegressor(random_state=42)
    model_xgb.fit(X_train, y_train)

    # write the trained model to your workspace in a file called
    # trainedmodel.pkl

    with open(os.path.join(model_path, 'trainedmodel.pkl'), 'wb') as file:
        pickle.dump(model_xgb, file)



if __name__ == '__main__':
    train_model()
    logging.info("Model successfully trained and saved")

