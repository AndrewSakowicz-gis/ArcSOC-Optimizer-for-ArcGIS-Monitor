class Pooling:
    def __init__(self, config, service_current):
        self._config=config
        self.service_current=service_current
        self._past_days=self._config["ArcSOCOptimizer"]["past_days"]
        self._high_usage_sec=self._config ["ArcSOCOptimizer"]["high_usage"]["avg_sec/day"]*self._past_days
        self._low_usage_sec=self._config["ArcSOCOptimizer"]["low_usage"]["avg_sec/day"]*self._past_days
        self._shared_to_dedicated_config=self._config["ArcSOCOptimizer"]["high_usage"]["shared_to_dedicated"]
        self._dedicated_to_shared_config=self._config["ArcSOCOptimizer"]["low_usage"]["dedicated_to_shared"]


        self.instance_type_proposed=self.service_current.instance_type_current
        if self.service_current.sec_sum!=None:
            self._pooling_proposed()
        #print (self.instance_type_proposed)
    def _pooling_proposed(self):       
        if self._dedicated_to_dedicated () or self._shared_to_dedicated ():
            self.instance_type_proposed="dedicated" 
        if self._dedicated_to_shared() or self._shared_to_shared():
            self.instance_type_proposed="shared" 
    
    def _shared_to_dedicated (self):
        if self.service_current.sec_sum>=self._high_usage_sec and self.service_current.supports_shared:
            return True
        return False
    def _dedicated_to_dedicated (self):
        instance_type_current=self.service_current.instance_type_current
        #instance_type_current=self._service_attributes["instance_type_current"]
        if instance_type_current=="dedicated" and self.service_current.supports_shared==False: 
            return True
        return False
    def _dedicated_to_shared(self):
        if self.service_current.supports_shared and self.service_current.sec_sum<=self._low_usage_sec and self._dedicated_to_shared_config:         
            return True
        return False
    def _shared_to_shared(self):
        instance_type_current=self.service_current.instance_type_current
        if instance_type_current=="shared" and self.service_current.sec_sum<=self._high_usage_sec:
            return True
        return False

  
    