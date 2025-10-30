import math, logging
log = logging.getLogger(__name__)
class Service_current:
    def __init__(self, service):
        
        self.folder=""
        self.service_name=service["attributes"]["name"]
        self._set_name()
        self.service_type=service["attributes"]["subtype"]
        self.instance_type_current=service["attributes"]["instance_type"]
        self.min_current=service["attributes"]["instances_min"]
        self.max_current=service["attributes"]["instances_max"]
        #self.provider=service["attributes"]["properties"]["provider"]
        #self.extensions=service["attributes"]["extensions"]
        self.supports_shared=self._supports_shared()
        self.instances_used=None
        self.sec_sum=None


        self._set_stats(service["metrics"])

    def _supports_shared(self):
        #if self.service_type!="MapServer" or self.provider in ["ArcObjects", "SDS"]: 
        if self.service_type!="MapServer" or self.folder in  ["System", "Utilities"]: 
            return False
        # for e in self.extensions:
        #     if e not in ["FeatureServer", "WFSServer","WMSServer"]:
        #         return False    

        return True
    def _set_name(self):
        temp=self.service_name.split("/")
        if len(temp)==2:
            self.folder=temp[0]
            self.service_name=temp[1]
    def _set_stats(self, service_metrics):
        rt_avg=0
        req_sum=0
        instances_used=0    
        for m in service_metrics: 

            if len(m["metrics_data"])==0: 
                msg=self.service_name + " len(m[metrics_data])==0"
                log.info(msg)
                continue
            if m["attributes"]["r_id"]=="requests_response_time_avg":
                rt_avg=m["metrics_data"][0]["attributes"]["AVG_value"] 
                msg=self.service_name + " requests_response_time_avg " + str(rt_avg)
                log.info(msg) 
                if rt_avg is None: 
                    rt_avg=0
                    msg=self.service_name + " rt_avg is None, setting to 0"
                    log.info(msg)
                    
            if m["attributes"]["r_id"]=="requests_received":
                req_sum=m["metrics_data"][0]["attributes"]["SUM_value"] 
                msg=self.service_name + " requests_received " + str(req_sum)
                log.info(msg )
                if req_sum is None:
                    req_sum=0
                    msg=self.service_name + "Requests Received is None, setting to 0"
                    log.info(msg)
            if m["attributes"]["r_id"]=="instances_used_avg":                     
                instances_used=m["metrics_data"][0]["attributes"]["MAX_value"] 
                msg=self.service_name + " instances_used_avg" + str(instances_used)
                log.info(msg)
                if instances_used is None: 
                    instances_used=0
                    msg=self.service_name + " Instances used avg is None, setting to 0"
                    log.info(msg)
                    
        self.sec_sum=rt_avg*req_sum      
        self.instances_used=math.ceil(instances_used)
        
