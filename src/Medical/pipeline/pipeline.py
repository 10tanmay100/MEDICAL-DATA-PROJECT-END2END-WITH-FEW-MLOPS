from Medical.components import DataIngestion,DataValidation,DataTransformation,ModelTrainer
from Medical.config import ConfigurationManager
from Medical.logger import logging 
from Medical.utils import read_data
from pathlib import Path
from Medical.constants import INGESTED_FOLDER_NAME
import os

STAGE_NAME="Pipeline Stage"


class RetrainPipeline:
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






if __name__=="__main__":
    try:
        logging.info(f">>>>>>> {STAGE_NAME} has started <<<<<<<")
        main()
        logging.info(f">>>>>>> {STAGE_NAME} has ended <<<<<<<")
    except Exception as e:
        raise e