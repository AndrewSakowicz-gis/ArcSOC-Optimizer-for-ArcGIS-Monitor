from modules.ArcSOCOptimizer import  pooling

import logging, sys
log = logging.getLogger(__name__)
class Service_proposed:
    def __init__(self, config, service_current, machines_started):
        self._config=config
        self.min_proposed=service_current.min_current
        self.max_proposed=service_current.max_current

        self._sec_sum=service_current.sec_sum
        self.instances_used=service_current.instances_used
        self._machines_started=machines_started
        self.instance_type_proposed=pooling.Pooling(config, service_current).instance_type_proposed
        self._min_max_proposed(service_current.min_current)
        self.instance_type_change=False

    def _min_max_proposed(self, min_current):
        if self.instance_type_proposed!="dedicated" or self._sec_sum==None: 
            return
        ###Not needing this check
        # if self.instance_type_proposed=="dedicated" and min_current==0:
        #     return
        past_days=self._config["ArcSOCOptimizer"]["past_days"]
        diff = self._config["ArcSOCOptimizer"]["limits"]["max_min_diff"]
        low_usage_sec=self._config["ArcSOCOptimizer"]["low_usage"]["avg_sec/day"]*past_days

        if self._sec_sum<=low_usage_sec:
            self.min_proposed=self._config["ArcSOCOptimizer"]["low_usage"]["dedicated_instance_min"]
            if self.instance_type_proposed=="dedicated" and min_current==0:
                self.min_proposed=min_current
        else:
            self.min_proposed=self.instances_used/self._machines_started
        self.max_proposed=self.min_proposed+diff

  