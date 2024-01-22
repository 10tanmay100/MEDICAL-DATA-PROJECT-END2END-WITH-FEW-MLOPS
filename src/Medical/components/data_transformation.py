from scipy.stats import ks_2samp
import shutil
import zipfile
import os
import pandas as pd
from Medical.exception import MedicalException
import botocore
from pathlib import Path
import joblib
from Medical.entity import *
from Medical.constants import *
from Medical.utils import read_yaml,read_data
from Medical.logger import logging
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from Medical.logger import logging

class DataTransformation:
    def __init__(self,ingest_config:DataIngestionConfig,valid_config:DataValidationConfig,transform_config:DataTransformationConfig):
        self.config=transform_config
        self.valid_config = valid_config
        self.ingest_config = ingest_config
        self.scaler=StandardScaler()
    def __train_test_split_(self):
        data_path=self.valid_config.validated_path
        logging.info(f"Taking the validated path,{data_path}")
        dataframes=[]
        for files in os.listdir(data_path):
            logging.info(f"Taking files,{files}")
            csv_data=Path(os.path.join(data_path,files))
            data=read_data(csv_data)
            logging.info(f"Reading {csv_data}")
            data["Class"]=files.split(".")[0]
            data=data.drop(["Unnamed: 0"],axis=1)
            logging.info(f"Dropping Unnamed: 0")
            dataframes.append(data)
        final_data=pd.concat(dataframes)
        logging.info(f"Concatenating dfs")
        X=final_data.drop(["Class"],axis=1)
        logging.info(f"Dropping Class")
        y=final_data["Class"]
        dict_={}
        for idx,cls in enumerate(y.unique()):
            dict_[cls]=idx
        y=y.map(dict_)
        return X,y
    def __scale_data(self,X,y):
        X,y=self.__train_test_split_()
        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0)
        logging.info("Splitting data into scaling function")
        y_train=y_train.reset_index(drop=True)
        logging.info("Resetting y train")
        y_test=y_test.reset_index(drop=True)
        logging.info("Resetting y test")
        scaled_train_path=os.path.join(self.config.transfromed_train_path,"train.csv")
        scaled_test_path=os.path.join(self.config.transfromed_test_path,"test.csv")
        print("X train shape----------->",X_train.shape)
        X_train_scaled=pd.concat([pd.DataFrame(self.scaler.fit_transform(X_train),columns=X_train.columns),y_train],axis=1).to_csv(scaled_train_path,index=False)
        logging.info(f"Training scaled csv ready and stored in {scaled_train_path}")
        X_test_scaled=pd.concat([pd.DataFrame(self.scaler.transform(X_test),columns=X_test.columns),y_test],axis=1).to_csv(scaled_test_path,index=False)
        logging.info("Testing scaled csv ready and stored in {scaled_test_path}")
        joblib.dump(self.scaler,os.path.join(self.config.scaler_model_path,"scaler.joblib"))
        logging.info(f"Dumping the scaler object to,{os.path.join(self.config.scaler_model_path,'scaler.joblib')}")

    def apply_transformation(self):
        X,y=self.__train_test_split_()
        self.__scale_data(X,y)

