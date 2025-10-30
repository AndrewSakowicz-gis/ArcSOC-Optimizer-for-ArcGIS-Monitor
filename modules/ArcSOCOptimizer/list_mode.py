from modules.ArcSOCOptimizer import ags_server, host, service_current, service_proposed, agm_api
from modules.User_Input import date_helper
import logging
log = logging.getLogger(__name__)
class List_mode:
    def __init__(self, config, url, token):
        self.config=config
        self.url=url
        self.token=token
        self._utc_now = date_helper.now_UTC_str()
        self.past_days=self.config["ArcSOCOptimizer"]["past_days"]
        self._utc=  date_helper.past_UTC_str(self.past_days,0,0)
        self.ags_server_obj=ags_server.Ags_server(config, url, token, self._utc, self._utc_now)
        self.machines_started=self.ags_server_obj.machines_started
        self._host=host.Host(config, url, token)
        self.list_view = self._list_view()
    def _list_view(self):
        observer_id=self.ags_server_obj.observer_id
        response=agm_api.run_observer(self.url, self.token,observer_id )
        log.info("observer run " + response.text)
        out=[]  
        self._host.set_stats(self._utc, self._utc_now) 
        memory_pass=self._host.memory_pass   
        memory_available_GB_min=self._host.memory_available_GB_min
        cpu_avg=self._host.cpu_avg
        for service in self.ags_server_obj.services:
            #if service["attributes"]["properties"]["provider"]=="SDS": continue    
            sc=service_current.Service_current(service)
            service_name=sc.service_name
            folder=sc.folder
            # if self._exclude(self.config, folder, service_name): 
            #     continue 
            service_type=sc.service_type
            instance_type_current=sc.instance_type_current
            instance_type_proposed=instance_type_current
            min_current=sc.min_current
            max_current=sc.max_current
            sec_sum=sc.sec_sum

            sp=service_proposed.Service_proposed(self.config,sc,self.machines_started)
            min_proposed=sp.min_proposed
            max_proposed=sp.max_proposed
            instance_type_proposed=sp.instance_type_proposed
            instances_used=sp.instances_used
            instance_type_change=False 
            min_max_change=False
              
            if instance_type_current!=instance_type_proposed and instance_type_proposed!=None:
                instance_type_change=True          
            if min_current!=min_proposed and instance_type_proposed=="dedicated": 
                min_max_change=True
            if instance_type_proposed=="shared": 
                min_proposed=max_proposed=min_max_change=None
            avg_sec_per_day=round(sec_sum/ self.past_days,2)
            temp={"folder":folder, "service":service_name, "type":service_type, "poolingCurrent":instance_type_current,"poolingProposed":instance_type_proposed,
            "avg_sec/day":avg_sec_per_day,"instancesUsed":instances_used,
            "minCurrent":min_current, "maxCurrent":max_current, "minProposed":min_proposed, "maxProposed":max_proposed, "memoryPass":memory_pass, "memAvailGBMin":memory_available_GB_min, "cpuAvg":cpu_avg, "poolingChange":instance_type_change, "minMaxChange":min_max_change}
            out.append(temp)
        return out
    # def _exclude(self,config, folder, service_name):
    #     if service_name in config["ArcSOCOptimizer"]["exclude"]["services"] or folder in config["ArcSOCOptimizer"]["exclude"]["folders"]:
    #         return True
    #     return False
    

     