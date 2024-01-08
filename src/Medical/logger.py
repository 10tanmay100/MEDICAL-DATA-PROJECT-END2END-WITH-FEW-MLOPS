#importing libraries
import os
import logging
import os
from datetime import datetime

#defining the log file name
log_file_name=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

#defining the log file path
LOG_FILE_PATH=os.path.join(os.getcwd(),"logs",log_file_name)

#creating the directory of logger
os.makedirs(LOG_FILE_PATH,exist_ok=True)
log_file_directory=os.path.join(LOG_FILE_PATH,log_file_name)

#Defining the log configurations
logging.basicConfig(filename=log_file_directory,level=logging.INFO,format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s")


