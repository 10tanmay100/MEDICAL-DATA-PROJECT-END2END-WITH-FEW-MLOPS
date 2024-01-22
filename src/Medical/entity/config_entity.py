#imporing libraries
from dataclasses import dataclass
from pathlib import Path

#defining the dataingestion configuration data types
@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir:Path
    S3_bucket_name:str
    raw_data_name:str
    local_data_file:Path
    unzip_dir:Path
    loose_files:Path
    raw_file_path:Path
    extracted_dir:Path

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir:Path
    validated_path:Path

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir:Path
    transfromed_train_path:Path
    transfromed_test_path:Path
    scaler_model_path:Path

@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir:Path

