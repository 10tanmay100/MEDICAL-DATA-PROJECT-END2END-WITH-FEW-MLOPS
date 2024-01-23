from Medical.utils import *
from Medical.entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
import boto3
import sys
from datetime import datetime
import os
from scipy.stats import ks_2samp
import shutil
from sklearn.model_selection import train_test_split,GridSearchCV
import zipfile
import numpy as np
import pandas as pd
from Medical.exception import MedicalException
import botocore
from Medical.constants import *
from Medical.logger import logging
from sklearn.metrics import precision_score,recall_score,f1_score
from mlflow.models.signature import ModelSignature, infer_signature
from sklearn.svm import SVC
import mlflow
import warnings
warnings.filterwarnings("ignore")


class ModelTrainer:
    def __init__(self,ingest_config:DataIngestionConfig,valid_config:DataValidationConfig,transform_config:DataTransformationConfig,config:ModelTrainerConfig):
        self.config = config
        self.ingest_config = ingest_config
        self.valid_config=valid_config
        self.transform_config = transform_config
        self.__models = load_config(Path(MODEL_JSON_PATH))
        self.__hyperparams = load_config(Path(HYP_JSON_PATH))

    def __tune_params(self):
        pass

    def train(self):
        try:
            mlflow.set_tracking_uri(uri=TRACKING_URI)
            now = datetime.now()
            #generating the folder based on the current datetime
            date_time = now.strftime("%m-%d-%Y-%H-%M-%S-%MS")
            print("The set tracking uri is ", mlflow.get_tracking_uri())
            exp_id = mlflow.create_experiment(
                name="create_exp_artifact"+date_time,
                tags={"version": "v1", "priority": "p1"},
                artifact_location=Path.cwd().joinpath("myartifacts").as_uri()
            )
            get_exp = mlflow.get_experiment(exp_id)

            train_path=Path(os.path.join(self.transform_config.transfromed_train_path,"train.csv"))
            X_tr=read_data(train_path)

            test_path=Path(os.path.join(self.transform_config.transfromed_test_path,"test.csv"))
            X_ts=read_data(test_path)

            X_train=X_tr.drop(["Class"],axis=1)

            X_test=X_ts.drop(["Class"],axis=1)

            y_train=X_tr["Class"]

            y_test=X_ts["Class"]

            for name, model in self.__models.items():
                with mlflow.start_run(experiment_id=exp_id):
                    logging.info(f"Looping through model:{name} and items:{model}")
                    pipeline=make_pipeline(model)
                    # mlflow.log_artifacts(train_path)
                    # mlflow.log_artifacts(test_path)

                    clf = GridSearchCV(pipeline, self.__hyperparams[name], cv=100)
                    mlflow.log_params(self.__hyperparams[name])
                    
                    logging.info(f"Applying Gridsearchcv for params:{self.__hyperparams[name]}")

                    clf.fit(X_train, y_train)
                    
                    logging.info("Fitting on the data")
                    print(f"Best parameters for {name}: {clf.best_params_}")

                    predictions = clf.predict(X_test)
                    logging.info("Predicting..")
                    precision=precision_score(y_test,predictions,average="micro")
                    recall=recall_score(y_test,predictions,average="micro")
                    f1=f1_score(y_test,predictions,average="micro")

                    mlflow.log_metric("Precision Score",precision)
                    mlflow.log_metric("Recall Score",recall)
                    mlflow.log_metric("F1 Score",f1)

                    signature = infer_signature(X_train, predictions)
                    input_example = {
                        "columns":np.array(X_train.columns),
                        "data": np.array(X_train.values)
                    }

                    # mlflow.log_metrics(r2_score(y_test,predictions))
                    model_path=os.path.join(self.config.root_dir,"model_"+name+".h5")
                    joblib.dump(clf,"model_"+name+".h5")
                    joblib.dump(clf,"model_"+name+".h5")
                    mlflow.sklearn.log_model(clf, model_path, signature=signature, input_example=input_example)
                    mlflow.log_artifacts("artifacts/")
                    logging.info(f"Dumping model {model_path}")
        except Exception as e:
            logging.error("Error while training",e)
            raise MedicalException(e,sys) from e



# def main():
#     models = get_models()
#     hyperparams = get_hyperparameters()

#     for name, model in models.items():
#         pipeline = make_pipeline(model)
#         clf = GridSearchCV(pipeline, hyperparams[name], cv=5)
#         clf.fit(X_train, y_train)
#         print(f"Best parameters for {name}: {clf.best_params_}")
#         predictions = clf.predict(X_test)
        