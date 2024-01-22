from Medical.components import DataIngestion
from Medical.config import ConfigurationManager
from Medical.logger import logging 

STAGE_NAME="Data Ingestion Stage"

def main():
    config=ConfigurationManager()
    data_ingestion_config=config.get_data_ingestion_config()
    data_ingestion=DataIngestion(config=data_ingestion_config)
    # data_ingestion.download_file()
    # data_ingestion.unzip_clean_data()
    data_ingestion.ingest_data()





if __name__=="__main__":
    try:
        logging.info(f">>>>>>> {STAGE_NAME} has started <<<<<<<")
        main()
        logging.info(f">>>>>>> {STAGE_NAME} has ended <<<<<<<")
    except Exception as e:
        raise e