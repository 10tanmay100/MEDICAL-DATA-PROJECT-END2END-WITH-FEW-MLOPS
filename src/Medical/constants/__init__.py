#importing library
from pathlib import Path


#defining the configuration yaml file path
CONFIG_FILE_PATH= Path("configs/config.yaml")
SCHEMA_FILE_PATH= Path("configs/schema.yaml")
INGESTED_FOLDER_NAME="Medical Data"
MODEL_JSON_PATH='configs/models.json'
HYP_JSON_PATH='configs/hyperparameters.json'
MODEL_NAME="model.h5"


TRACKING_URI="http://3.110.101.43:5000/"