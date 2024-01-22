from Medical.components import DataIngestion,DataValidation
from Medical.config import ConfigurationManager
from Medical.logger import logging 
from Medical.utils import read_data
from pathlib import Path
from Medical.constants import INGESTED_FOLDER_NAME
import os

STAGE_NAME="Data Validation Stage"

def main():
    config=ConfigurationManager()
    data_ingestion_config=config.get_data_ingestion_config()
    data_ingestion=DataIngestion(config=data_ingestion_config)
    data_ingestion.download_file()
    data_ingestion.unzip_clean_data()
    data_validation_config=config.get_data_validation_config()
    data_validation=DataValidation(ingest_config=data_ingestion_config,valid_config=data_validation_config)
    # for csvs in os.listdir(data_ingestion_config.raw_file_path):
    #     csv_path=Path(os.path.join(data_ingestion_config.raw_file_path,csvs))
    #     dataframe=read_data(csv_path)
    #     if data_validation.validate_number_of_columns(dataframe):
    #         data_path=os.path.join(data_validation_config.validated_path,csvs)
    #         read_data(csv_path).to_csv(data_path)
    data_validation.apply_validation()





if __name__=="__main__":
    try:
        logging.info(f">>>>>>> {STAGE_NAME} has started <<<<<<<")
        main()
        logging.info(f">>>>>>> {STAGE_NAME} has ended <<<<<<<")
    except Exception as e:
        raise e