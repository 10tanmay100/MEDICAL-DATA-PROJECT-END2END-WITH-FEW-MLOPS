from Medical.entity import DataIngestionConfig
import boto3
import sys
from datetime import datetime
import os
import shutil
import zipfile
from Medical.exception import MedicalException
import botocore
from Medical.constants import *
from Medical.logger import logging
import io
import os

class DataIngestion:
    def __init__(self,config:DataIngestionConfig):
        self.config = config
        self.s3 = boto3.resource('s3')
        self.s3_client = boto3.client('s3')
        self.bucket_name=self.config.S3_bucket_name 
        self.KEY = self.config.raw_data_name
    
    def __create_zip_in_memory(self,files):
        try:
            
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
                for file in files:
                    zip_file.write(file)
            zip_buffer.seek(0)
            logging.info("creating zip memory..")
            return zip_buffer
        except Exception as e:
            logging.error(f"Error, {e}")
            raise MedicalException(e,sys) from e
    def __upload_zip_to_s3(self,zip_buffer, zip_name):
        
        try:
            bucket = self.s3.Bucket(self.bucket_name)
            bucket.upload_fileobj(zip_buffer, zip_name)
            logging.info("New Data Updated in s3")
        except Exception as e:
            logging.error(f"Error, {e}")
            raise MedicalException(e,sys) from e

    def __download_file(self):
        try:
            objects = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix="data")['Contents']
            logging.info("Fetching objects from Bucket")
            files = []
            for obj in objects:
                file_name = obj['Key']
                if file_name.endswith('.csv'):
                    logging.info(f"Fetching csv files from {file_name}")
                    os.makedirs("Medical Data",exist_ok=True)
                    download_path=os.path.join("Medical Data",file_name.split("/")[1])
                    self.s3_client.download_file(self.bucket_name, file_name, download_path)
                    logging.info("Downloading file from s3")
                    files.append(download_path)
            zip_buffer = self.__create_zip_in_memory(files)
            self.__upload_zip_to_s3(zip_buffer,self.KEY)
            
            download_file_path = os.path.join(self.config.local_data_file)
            self.s3.Bucket(self.bucket_name).download_file(self.KEY, download_file_path)
            logging.info("Downloaded zip file %s" % download_file_path)
            # return files
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                logging.error("Object Does not exist")
                raise MedicalException(e,sys) from e
            else:
                logging.error(e)
                raise MedicalException(e,sys) from e
    

    def __unzip_clean_data(self):
        try:
            #detecting the current datetime
            now = datetime.now()
            #generating the folder based on the current datetime
            date_time = now.strftime("%m-%d-%Y-%H-%M-%S-%MS")

            # Open the ZIP file for reading
            with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
                # Extract all the contents of the ZIP file into the specified directory
                zip_ref.extractall(self.config.extracted_dir)
                logging.info(f"Successfully extracted the ZIP file to {os.path.join(self.config.extracted_dir)}")
        except Exception as e:
            logging.error(f"Error, {e}")
            raise MedicalException(e,sys) from e
        
    def ingest_data(self):
        self.__download_file()
        self.__unzip_clean_data()
