
from modules.ArcSOCOptimizer import agsadmin, host, agm_api
from modules.User_Input import date_helper

import logging
log = logging.getLogger(__name__)
class Edit_mode:
    def __init__(self, list_mode):
        self.config=list_mode.config
        self.url=list_mode.url 
        self.token=list_mode.token
        self.address=list_mode.config["ArcSOCOptimizer"]["component_address"]
        self.edit=list_mode.config["ArcSOCOptimizer"]["edit"]
        self.past_days=list_mode.config["ArcSOCOptimizer"]["past_days"]
        self.list_mode=list_mode
        self._edit()
        self.edit_view=self.list_mode.list_view
    
    def _edit (self):
        observer_id=self.list_mode.ags_server_obj.observer_id
        #observerObject=observers.Observers(self.url, self.token)
        agsadminObject=self._get_agsadminObject()
        hostObject=host.Host(self.config, self.url, self.token)
        for i in self.list_mode.list_view:
            utc_now = date_helper.now_UTC_str()
            utc=  date_helper.past_UTC_str(self.past_days,0,0)
            hostObject.set_stats(utc, utc_now)
            memory_pass=hostObject.memory_pass
            memory_available_GB_min=hostObject.memory_available_GB_min
            cpu_avg=hostObject.cpu_avg

            i["memory_pass"]=memory_pass
            i["memAvailGBMin"]=memory_available_GB_min
            if memory_pass==False: 
                log.info("memory_pass False " +str(memory_available_GB_min))
                continue
            folder=i["folder"]
            service_name=i["service"]
            service_type=i["type"]
            min_proposed=i["minProposed"]
            max_proposed=i["maxProposed"]
            
            if i["poolingChange"] and folder not in ["System", "Utilities"]:
                if i["poolingProposed"]=="dedicated":
                    response = agsadminObject.shared_to_dedicated(folder, service_name, service_type)
                    i["poolingChange"]=response.text
                    msg=service_name + " shared_to_dedicated " + response.text
                    print(msg)
                    log.info(msg)
                if i["poolingProposed"]=="shared":
                    response = agsadminObject.dedicated_to_shared(folder, service_name, service_type)
                    i["poolingChange"]=response.text
                    msg=service_name + " dedicated_to_shared " + response.text
                    print(msg)
                    log.info(msg)

            if i["minMaxChange"] :
                response = agsadminObject.edit_instances(folder, service_name, service_type, min_proposed, max_proposed)
                i["minMaxChange"]=response.text
                msg=service_name + " minMaxChange " + response.text
                print(msg)
                log.info(msg)
            if i["poolingChange"] or i["minMaxChange"]: 
                response=agm_api.run_observer(self.url, self.token,observer_id)
                log.info("observer run " + response.text)
        
    def _get_agsadminObject(self):
        site_url=self.config["ArcSOCOptimizer"]["arcgis_server"]["server_admin_url"]
        token_url=self.config["ArcSOCOptimizer"]["arcgis_server"]["token_url"]
        client=self.config["ArcSOCOptimizer"]["arcgis_server"]["client"]
        referer=self.config["ArcSOCOptimizer"]["arcgis_server"]["referer"]
        username=self.config["ArcSOCOptimizer"]["arcgis_server"]["username"]
        password=self.config["ArcSOCOptimizer"]["arcgis_server"]["password"]  
        agsObject=agsadmin.AGSAdmin(site_url, token_url, username, password, client, referer) 
        return agsObject
    
    
