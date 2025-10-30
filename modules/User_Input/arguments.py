import argparse
class Arguments:
    def __init__(self):
        self.file=''
        self.operation=""              
        self.__check_arg(args=None)
    def __check_arg(self,args=None):
        parser = argparse.ArgumentParser()       
        #parser.add_argument('-file', '--file', help='path to config file, default config.json', default='config.json')  
        parser.add_argument('-f', '--file', help='path to input file', required=True)  
        results=  parser.parse_args(args)       
        self.file=results.file
        

        
    