import sys
import logging
logging.basicConfig(filename='error.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
def error_message_detail(error,error_details:sys):
    _,_,exc_tb = error_details.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occoured in python script name [{0}] line number: [{1}] error message[{2}]".format(
    file_name,exc_tb.tb_lineno,str(error))
    return error_message

class CustomException(Exception):
    def __init__(self, error_message,error_details:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message,error_details=error_details)
        logging.error(self.error_message)
        
    def __str__(self):
        return self.error_message

if __name__ == '__main__':
    try:
        a=1/0
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise CustomException(e,sys)
