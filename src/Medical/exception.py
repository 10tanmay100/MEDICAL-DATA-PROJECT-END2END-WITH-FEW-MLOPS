#importing libraries
import sys

#defining the function that will generate custom error message
def error_message_detail(error,error_detail:sys):
          _,_,exc_tb=error_detail.exc_info()

          file_name=exc_tb.tb_frame.f_code.co_filename
          error_message=f"Error occured python script name {file_name} line number {exc_tb.tb_lineno} error message {str(error)}"

          return error_message

#Defining my own Exception Class
class MedicalException(Exception):
          def __init__(self,error_message,error_detail:sys):
                    super().__init__(error_message)
                    self.error_message = error_message_detail(error_message,error_detail=error_detail)