from modules.ArcSOCOptimizer import agm_api
import logging, sys, datetime
log = logging.getLogger(__name__)
class Ags_server:
    def __init__(self, config, url, token, utc, utc_now):
        self._config=config
        self._url=url
        self._token=token
        self._utc=utc
        self._utc_now= utc_now
        self.observer_id=None
        self.services=[]
        self.machines_started=None      
        self._set_stats()
    def _set_stats(self):
        address=self._config["ArcSOCOptimizer"]["component_address"]
        response=agm_api.query_by_address_type(self._url, self._token, address, "arcgis_server")
        if response.status_code in [500,400]:
            msg= "Error query_by_address for "+ str(address) + ":" + response.text
            log.error(msg)
            sys.exit()        
        response= response.json()
        print (response, 11111111111111111111111111111)

        self.observer_id=self._get_observer_id(response["features"][0]["observers"])
        server_id=response["features"][0]["attributes"]["id"]
        services=[]
        for s in response["features"][0]["children"]:
            name=s["attributes"]["name"]
            if self._exclude(name)==False:
                services.append(s)
        
        response=agm_api.get_component_resource(self._url, self._token, server_id)

        machines=response["attributes"]["properties"]["machines"]   
        ##########self.machines_started=self._machines_started(machines)
        self.machines_started=len(machines)
        ids=self._get_ids(services)
        paging_size=50
        if "paging_size" in self._config["server"]:
            paging_size=self._config["server"]["paging_size"] 
        ids_bins=self._bin(ids, paging_size)
        current_count=0
        for i in ids_bins:
            ids_tuple=tuple(i)

            if len(i)==1: 
                ids_tuple="("+str(i[0])+")" 
            current_count=current_count+len(ids_tuple)
            msg="metrics for " + str(current_count) +" of total "+str(len(ids)) + " services"
            print (datetime.datetime.now(), msg)
            log.info(msg)
            response=agm_api.get_metric_data_tuple(self._url, self._token, ids_tuple,self._utc, self._utc_now)
            response= response.json()
 
            for i in response["features"]:
                self.services.append(i)
    

        ##########response=agm_api.get_metric_data(self._url, self._token, server_id,self._utc, self._utc_now)
        
        # for s in services:
        #     service_id=s["attributes"]["id"]
        #     name=s["attributes"]["name"]
        #     msg="metric stats for " + str(name)
        #     print (datetime.datetime.now(), msg)
        #     response=agm_api.get_comp_data(self._url, self._token, service_id,self._utc, self._utc_now)
        #     response= response.json()
        #     self.services.append(response["features"][0])

    def _machines_started(self, machines):
        count=0
        for m in machines:
            if m["system_state"]=="started":
                count += 1
        return count
    def _get_observer_id(self, observers):
        id=None
        for i in observers:
            
            if i["attributes"]["name"]=="Inventory":
                id= i["attributes"]["id"]
        return id   
    def _exclude(self, service_name):
        out=False
        temp=service_name.split("/")
        folder=""
        service=service_name
        if len(temp)==2:
            folder=temp[0]
            service=temp[1]     
        if service in self._config["ArcSOCOptimizer"]["exclude"]["services"] or folder in self._config["ArcSOCOptimizer"]["exclude"]["folders"]:
            out=True 
        return out
    def _get_ids(self, services):
        ids=[]
        for s in services:
            service_id=s["attributes"]["id"]
            ids.append(service_id)
        return ids
    def _bin(self, mylist, bin_size):
        out=[]
        for i in range(0, len(mylist), bin_size):
            out.append(mylist[i:i+bin_size])
        return out