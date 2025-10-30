from modules.ArcSOCOptimizer import  agm_api
import logging, sys
log = logging.getLogger(__name__)
class Host:
    def __init__(self, config, url, token):
        self.url=url
        self.token=token
        self._config=config  
        self.memory_pass=True
        self.memory_available_GB_min=None
        self.cpu_avg=None

    def set_stats(self, utc, utc_now):   
        for host_address in self._config["ArcSOCOptimizer"]["arcgis_server"]["host_address"]:
            host_id=self._host_id_from_address(host_address)
            host_data=agm_api.get_metric_data(self.url, self.token, host_id,utc, utc_now)
            host_data= host_data.json()
            cpu_array=[]
            for c in host_data["features"]:
                if c["attributes"]["type"]=="host":
                    for m in c["metrics"]:
                        if m["attributes"]["name"]=="Memory Available":
                            memory_available_GB=m["metrics_data"][0]["attributes"]["MIN_value"] 
                            if self.memory_available_GB_min==None: 
                                self.memory_available_GB_min=memory_available_GB
                            else:
                                self.memory_available_GB_min=min(self.memory_available_GB_min, memory_available_GB)
                            if memory_available_GB<=self._config["ArcSOCOptimizer"]["limits"]["memory_available_GB"]:
                                self.memory_pass=False    
                        if m["attributes"]["name"]=="CPU Utilized":  
                            cpu_array.append(m["metrics_data"][0]["attributes"]["AVG_value"]) 
        self.cpu_avg = round(sum(cpu_array)/len(cpu_array),2)            

    def _host_id_from_address(self, host_address):  
        response=agm_api.query_by_address_type(self.url, self.token, host_address, "host")
        if response.status_code in [500,400]:
            msg= "Error query_by_address for "+ str(a) + ":" + response.text
            log.error(msg)
            sys.exit()        
        response= response.json()
        return response["features"][0]["attributes"]["id"]