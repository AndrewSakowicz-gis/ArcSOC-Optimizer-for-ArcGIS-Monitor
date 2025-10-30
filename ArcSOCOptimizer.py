
import traceback,logging, sys,urllib3
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from modules import report_builder
version='20241002.0'
def main(argv=None):  
    try:  
        LOG_LEVEL=logging.INFO
        #logging.basicConfig(filename="AGMAdminUtility.log", filemode='a', level=LOG_LEVEL, format='%(asctime)s %(levelname)s: %(filename)s:%(lineno)s:%(funcName)20s(): %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')  
        logging.basicConfig(filename="./logs/ArcSOCOptimizer.log", filemode='a', level=LOG_LEVEL, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p') 
        logging.info('version:'+version)       
        print ('version:'+version)       
        report_builder.Report_Builder() 
    except Exception as error:
        print (error)
        print (traceback.print_exc())
        logging.error(error)
        logging.exception(traceback.print_exc())  
        sys.exit(1)  

if __name__ == "__main__":
    main(None)

#pyinstaller.exe ArcSOCOptimizer.py --onefile
