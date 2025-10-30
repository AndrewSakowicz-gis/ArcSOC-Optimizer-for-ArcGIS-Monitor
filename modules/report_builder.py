
from modules.User_Input import arguments, user_inputs
from modules.ArcSOCOptimizer import list_mode, edit_mode
import logging,uuid, csv, copy, datetime
log = logging.getLogger(__name__)
class Report_Builder:
    def __init__(self):      
        f = arguments.Arguments().file
        log.info("Start")
        log.info("Arguments: " + f )
        
        user_inputs_ob=user_inputs.Inputs(f)   
        self._config=user_inputs_ob.config
        self._url=user_inputs_ob.url
        self._token=user_inputs_ob.token
        self.execute=self._execute()

    def _execute(self):
        config_deepcopy =copy.deepcopy (self._config["ArcSOCOptimizer"])
        #redact password in logging
        config_deepcopy["arcgis_server"]["password"]="xxx"
        log.info(config_deepcopy)
        list_obj=list_mode.List_mode(self._config, self._url, self._token)
        out= list_obj.list_view
        log.info("list")
        log.info(out)
        headings={}
        if len(out)>0:
            headings =out[0].keys()
        folder = "reports"
        edit=self._config["ArcSOCOptimizer"]["edit"]
        mode="list"
        if edit:
            mode="edit"
            log.info("edit")
            edit_obj=edit_mode.Edit_mode(list_obj)
            out=edit_obj.edit_view  
            log.info(out)
        days=self._config["ArcSOCOptimizer"]["past_days"]
        component_address=self._config["ArcSOCOptimizer"]["component_address"]
        server_machine=component_address.split("/")[2].split(":")[0]
        d=datetime.datetime.now()
        d=d.strftime("%Y_%m_%d_%H_%M_%S")
        file=folder +"/"+server_machine+"_"+str(days)+"_"+mode + "_" +str(d)+".csv"
        with open(file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = headings)
            writer.writeheader()
            writer.writerows(out)
            # for r in out:
            #     writer.writerow(r)

        log.info(file)
       

   
       
        
