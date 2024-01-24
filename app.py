from flask import Flask, request, jsonify, render_template,redirect
import joblib
import boto3
from Medical.utils import read_yaml
from Medical.constants import CONFIG_FILE_PATH
from Medical.pipeline import RetrainPipeline
from Medical.components import DataIngestion,DataValidation,DataTransformation,ModelTrainer
from Medical.config import ConfigurationManager
from Medical.logger import logging 
from Medical.utils import read_data
from pathlib import Path
from Medical.constants import INGESTED_FOLDER_NAME
import os


def main():
    config=ConfigurationManager()
    data_ingestion_config=config.get_data_ingestion_config()
    data_ingestion=DataIngestion(config=data_ingestion_config)
    data_ingestion.ingest_data()
    data_validation_config=config.get_data_validation_config()
    data_validation=DataValidation(ingest_config=data_ingestion_config,valid_config=data_validation_config)
    data_validation.apply_validation()
    data_transformation_config=config.get_data_transformation_config()
    data_transformation=DataTransformation(ingest_config=data_ingestion_config,valid_config=data_validation_config,transform_config=data_transformation_config)
    # train_inputs,target_inputs=data_transformation.train_test_split_()
    # data_transformation.scale_data(train_inputs,target_inputs)
    data_transformation.apply_transformation()
    model_trainer_config=config.get_model_trainer_config()
    model_trainer=ModelTrainer(ingest_config=data_ingestion_config,valid_config=data_validation_config,transform_config=data_transformation_config,config=model_trainer_config)
    model_trainer.train()

app = Flask(__name__)

# Load your trained model (example: model.pkl)
model = joblib.load("model_LogisticRegression.h5")

cfg=read_yaml(CONFIG_FILE_PATH)
retrain=RetrainPipeline()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    features = [request.form.get("P_incidence"), request.form.get("P_tilt"), request.form.get("L_angle"), request.form.get("S_slope"), request.form.get("P_radius"), request.form.get("S_Degree")]
    prediction = model.predict([features])
    type_=None
    if prediction[0]==0:
        type_="Normal"
    elif prediction[0]==1:
        type_="Type_H"
    elif prediction[0]==2:
        type_="Type_S"
    else:
        return "pass"
    return render_template('index.html',prediction_text=type_)


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5000)