from Medical.constants import *
import sys
import os
from Medical.utils import read_yaml,create_directories
from Medical.entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from Medical.exception import MedicalException
from datetime import datetime
class ConfigurationManager:
    def __init__(
        self, 
        config_filepath = CONFIG_FILE_PATH):
        self.config = read_yaml(config_filepath)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        try:
            #detecting the current datetime
            now = datetime.now()
            #generating the folder based on the current datetime
            date_time = now.strftime("%m-%d-%Y-%H-%M-%S-%MS")
            #defining the unzipped extraction directory
            extracted_dir=os.path.join(config.unzip_dir,str(date_time))
            #path of extracted raw files
            raw_file_path=os.path.join(config.unzip_dir,str(date_time),INGESTED_FOLDER_NAME)
            create_directories([config.root_dir])
            data_ingestion_config = DataIngestionConfig(
                root_dir=config.root_dir,
                S3_bucket_name=config.S3_bucket_name,
                raw_data_name=config.raw_data_name,
                local_data_file=config.local_data_file,
                unzip_dir=config.unzip_dir,
                loose_files=config.loose_files,
                raw_file_path=raw_file_path,
                extracted_dir=extracted_dir
            )

            return data_ingestion_config
        except Exception as e:
            raise MedicalException(e,sys) from e
    def get_data_validation_config(self):
        try:
            config=self.config.data_validation
            #detecting the current datetime
            now = datetime.now()
            #generating the folder based on the current datetime
            date_time = now.strftime("%m-%d-%Y-%H-%M-%S-%MS")
            #deining the validate local data file path
            validated_path=os.path.join(config.root_dir,str(date_time),INGESTED_FOLDER_NAME)
            #creating the directories
            create_directories([validated_path])
            data_validation_config=DataValidationConfig(
                root_dir=config.root_dir,
                validated_path=Path(validated_path))

            return data_validation_config
        except Exception as e:
            raise MedicalException(e,sys) from e
    def get_data_transformation_config(self):
        try:
            config=self.config.data_transformation
            #detecting the current datetime
            now = datetime.now()
            #generating the folder based on the current datetime
            date_time = now.strftime("%m-%d-%Y-%H-%M-%S-%MS")
            #deining the validate local data file path
            transformed_path=os.path.join(config.root_dir,str(date_time))
            train_transformed_path=os.path.join(transformed_path,"train")
            test_transformed_path=os.path.join(transformed_path,"test")
            transformed_model_path=os.path.join(transformed_path,"model_scaler")

            #creating all directories
            create_directories([train_transformed_path,test_transformed_path,transformed_model_path])

            data_transformation_config=DataTransformationConfig(root_dir=Path(transformed_path),transfromed_train_path=Path(train_transformed_path),transfromed_test_path=Path(test_transformed_path),scaler_model_path=Path(transformed_model_path))

            return data_transformation_config
        except Exception as e:
            raise MedicalException(e,sys) from e
        
    def get_model_trainer_config(self):
        try:
            config=self.config.model_trainer
            #detecting the current datetime
            now = datetime.now()
            #generating the folder based on the current datetime
            date_time = now.strftime("%m-%d-%Y-%H-%M-%S-%MS")
            #deining the validate local data file path
            model_dir_path=os.path.join(config.root_dir,str(date_time))
            

            #creating all directories
            create_directories([model_dir_path])

            model_trainer_config=ModelTrainerConfig(root_dir=Path(model_dir_path))

            return model_trainer_config
        except Exception as e:
            raise MedicalException(e,sys) from e