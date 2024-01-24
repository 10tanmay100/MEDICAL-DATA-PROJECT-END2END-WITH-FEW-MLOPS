from Medical.entity import DataIngestionConfig,DataValidationConfig
import boto3
import sys
from datetime import datetime
import os
from scipy.stats import ks_2samp
import shutil
import zipfile
import pandas as pd
from Medical.exception import MedicalException
import botocore
from Medical.constants import *
from Medical.utils import read_yaml,read_data
from Medical.logger import logging

class DataValidation:
    def __init__(self,ingest_config:DataIngestionConfig,valid_config:DataValidationConfig):
        self.config = valid_config
        self.ingest_config = ingest_config
        self.__schema_config = read_yaml(SCHEMA_FILE_PATH)

    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            logging.info("Number of columns validation started!!!")
            number_of_columns=len(self.__schema_config["columns"])
            if len(dataframe.columns)==number_of_columns:
                    logging.info(f"data frame columns and number of columns checking passed...->> {len(dataframe.columns)==number_of_columns}")
                    logging.info("Number of columns validation ended!!!")
                    return True
            else:
                    logging.info(f"data frame columns and number of columns checking failed...->> {len(dataframe.columns)==number_of_columns}")
                    logging.info("Number of columns validation ended!!!")
                    return False
        except Exception as e:
            logging.error("validate number of columns check has some issue..")
            raise MedicalException(e,sys) from e
        
    def apply_validation(self):
        for csvs in os.listdir(self.ingest_config.raw_file_path):
            csv_path=Path(os.path.join(self.ingest_config.raw_file_path,csvs))
            dataframe=read_data(csv_path)
            if self.validate_number_of_columns(dataframe):
                data_path=os.path.join(self.config.validated_path,csvs)
                read_data(csv_path).to_csv(data_path)
                print("Reading..Done")
                