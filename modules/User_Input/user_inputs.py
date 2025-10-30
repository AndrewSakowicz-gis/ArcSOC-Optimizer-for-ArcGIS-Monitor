import base64, json, uuid
from modules.ArcSOCOptimizer import agm_api
from modules.User_Input import time
import logging
log = logging.getLogger(__name__)
class Inputs:
    def __init__(self, f):          
        self.config=self._set_config(f)    
        self.url = self._set_url(self.config["server"]["url"])
        self.token=self._get_token()
    
    def _read_config_file(self, fileName):    
        with open(fileName, "r") as jsonfile:          
            config = json.load(jsonfile)
            return config   
    def _set_encoding(self, config):     
        if "password_encoding" in config["server"] and config["server"]["password_encoding"]:       
                config["server"]["password"]=base64.b64decode(config["server"]["password"]).decode('utf-8') 
        if "password_encoding" in config["ArcSOCOptimizer"]["arcgis_server"] and config["ArcSOCOptimizer"]["arcgis_server"]["password_encoding"]: 
            config["ArcSOCOptimizer"]["arcgis_server"]["password"]=base64.b64decode(config["ArcSOCOptimizer"]["arcgis_server"]["password"]).decode('utf-8') 
        return config    
    
    
    def _set_config(self, file):
        config=self._read_config_file(file)
        config=self._set_encoding(config)
        return config
    
    
    def _get_token(self):
        username = self.config["server"]["username"]
        password = self.config["server"]["password"]
        response= agm_api.get_token(self.url, username, password)
        if response.status_code in [500,400]:
            msg= "Error getting token. "+response.text
            raise Exception(msg)
        return response.json()['access_token']  
                                            
    def _set_url(self, url):
        temp=url.split("/")
        if len(temp) not in [3, 4]: raise Exception("Invalid url:"+str(url))
        if len(temp)==3: return url+"/arcgis"
        if len(temp)==4: return url
