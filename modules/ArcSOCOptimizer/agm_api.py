import requests, logging, datetime, sys, json
log = logging.getLogger(__name__)
def query_by_address_type(url, token, address, type):
    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "+ token
    }
    route = "/monitoring/components/query"
    clause = "address_internal = '{}' and type = '{}'".format(address, type)
    payload = {"where": clause, "including": [{"resource": "children"}, {"resource":"labels"},{"resource": "observers"}]}
    response = requests.request("POST", url + route, json=payload, headers=headers, verify=False)       
    return response
def get_token(url, username,password ):
    payload = {
    "username": username,
    "password": password,
    "refresh_token": "",
    "issue_refresh_token": None,
    "exchange_refresh_token": None
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer"
    }
    route = "/auth/token"
    response = requests.request("POST", url + route, json=payload, headers=headers, verify=False)
    return response
def run_observer(url, token, id):
    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "+ token
    }
    route = "/monitoring/observers/run"
                
    payload = {
        "id": id
        }
    response = requests.request("POST", url + route, json=payload, headers=headers, verify=False)
    return response

def get_metric_data(url, token, componentId, utc1_str,utc2_str, test=1):
    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "+ token
    }
    route = "/monitoring/components/query"
    whereTime="(observed_at BETWEEN TIMESTAMP '{}'  AND TIMESTAMP '{}')".format(utc1_str,utc2_str )
    whereAlert="( (closed_at > TIMESTAMP '{}'  AND closed_at <= TIMESTAMP '{}') or closed_at IS NULL)".format(utc1_str,utc2_str)
    metricData=[
                    {"resource": "alerts",
                        "where":whereAlert
                    },
                    {
                    "resource": "metrics_data",
                    "where": whereTime,
                    "groupByFieldsForStatistics": ["metric_id"],
                    "outStatistics": [
                        {
                            "statisticType": [
                                "count",
                                "avg",
                                "min",
                                "max",
                                "sum",
                                "stddev"
                            ],
                            "onStatisticField": "value"
                        }
                        ]
                    }]
    

    
    payload = {
            "where": "id='{}'".format(componentId),
            "including": [
                {
                    "resource": "metrics",
                    "where": "1=1",
                    "including": metricData

                },
                
                {"resource": "children",
                    "including": [
                    
                    {
                        "resource": "metrics",
                        "where": "1=1",
                        "including": metricData
                    }
                ]
                }
                
            ]
        }

    response = requests.request("POST", url + route, json=payload, headers=headers, verify=False)
    if response.status_code in [500,400] or is_json(response)==False or "features" not in response.json() or len(response.json()["features"])==0 :
    #if response.status_code in [500,400] or len(response.json()["features"])==0:
        msg= "Error getting get_metric_data for componentId: " + str(componentId) + " msg:" +str(response.text) + " "+url + route + " "+ str(payload)
        print (datetime.datetime.now(), msg)
        log.error(msg)
        if test==1: 
            msg="Retrying"
            print (datetime.datetime.now(), msg)
            get_metric_data(url, token, componentId, utc1_str,utc2_str, 2)
        #raise Exception(msg)
    else:
        #log.info(payload)
        return response
    return response
def get_metric_data_tuple(url, token, componentId_tuple, utc1_str,utc2_str, test=1):
    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "+ token
    }
    route = "/monitoring/components/query"
    whereTime="(observed_at BETWEEN TIMESTAMP '{}'  AND TIMESTAMP '{}')".format(utc1_str,utc2_str )
    whereAlert="( (closed_at > TIMESTAMP '{}'  AND closed_at <= TIMESTAMP '{}') or closed_at IS NULL)".format(utc1_str,utc2_str)
    metricData=[
                    {
                    "resource": "metrics_data",
                    "where": whereTime,
                    "groupByFieldsForStatistics": ["metric_id"],
                    "outStatistics": [
                        {
                            "statisticType": [
                               
                                "avg",
                                "max",
                                "sum",
                            ],
                            "onStatisticField": "value"
                        }
                        ]
                    }]
    

    
    payload = {
            "where": "id in {}".format(componentId_tuple),
            "including": [
                {
                    "resource": "metrics",
                    "where": "r_id in ('requests_response_time_avg','requests_received', 'instances_used_avg')",
                    "including": metricData

                }
            ]
        }
    # print (url + route)
    # print (json.dumps(payload), "component_resource.py 11111111111111111111111111111111111111111111111111111111111111111111111")
    response = requests.request("POST", url + route, json=payload, headers=headers, verify=False)
    if response.status_code in [500,400] or is_json(response)==False or "features" not in response.json() or len(response.json()["features"])==0 :
    #if response.status_code in [500,400] or len(response.json()["features"])==0:
        msg= "Error getting get_metric_data for componentId: " + str(componentId_tuple) + " msg:" +str(response.text) + " "+url + route + " "+ str(payload)
        print (datetime.datetime.now(), msg)
        log.error(msg)
        if test==1: 
            msg="Retrying"
            print (datetime.datetime.now(), msg)
            get_metric_data_tuple(url, token, componentId_tuple, utc1_str,utc2_str, 2)
        #raise Exception(msg)
    else:
        #log.info(payload)
        return response
    return response

def get_comp_data(url, token, componentId, utc1_str,utc2_str, test=1):
    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "+ token
    }
    route = "/monitoring/components/query"
    whereTime="(observed_at BETWEEN TIMESTAMP '{}'  AND TIMESTAMP '{}')".format(utc1_str,utc2_str )
    whereAlert="( (closed_at > TIMESTAMP '{}'  AND closed_at <= TIMESTAMP '{}') or closed_at IS NULL)".format(utc1_str,utc2_str)
    metricData=[
                    {
                    "resource": "metrics_data",
                    "where": whereTime,
                    "groupByFieldsForstatistics": "metric_id",
                    "outStatistics": [
                        {
                            "statisticType": [
                               
                                "avg",
                                "max",
                                "sum",
                            ],
                            "onStatisticField": "value"
                        }
                        ]
                    }]
    

    
    payload = {
            "where": "id='{}'".format(componentId),
            "including": [
                {
                    "resource": "metrics",
                    "where": "r_id in ('requests_response_time_avg','requests_received', 'instances_used_avg')",
                    "including": metricData

                }
            ]
        }

    response = requests.request("POST", url + route, json=payload, headers=headers, verify=False)
    if response.status_code in [500,400] or is_json(response)==False or "features" not in response.json() or len(response.json()["features"])==0 :
    #if response.status_code in [500,400] or len(response.json()["features"])==0:
        msg= "Error getting get_metric_data for componentId: " + str(componentId) + " msg:" +str(response.text) + " "+url + route + " "+ str(payload)
        print (datetime.datetime.now(), msg)
        log.error(msg)
        if test==1: 
            msg="Retrying, consider reducing paging_size"
            print (datetime.datetime.now(), msg)
            log.error(msg)
            get_metric_data(url, token, componentId, utc1_str,utc2_str, 2)
        #sys.exit(1) 
        #raise Exception(msg)
    else:
        #log.info(payload)
        return response
    return response


def get_component_resource(url, token, component_id):
    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "+ token
    }
    route = "/monitoring/components/"+str(component_id)
    payload = {}
  
    response = requests.request("GET", url + route, json=payload, headers=headers, verify=False)    
    # print (url + route)
    # print (json.dumps(payload), "component_resource.py 11111111111111111111111111111111111111111111111111111111111111111111111")
    if response.status_code in [500,400] or is_json(response)==False or "attributes" not in response.json():
    #if response.status_code in [500,400] or len(response.json()["features"])==0:
        msg= "Error get_component_resource for " + str(id) +  " msg:" +str(response.text) + " "+url + route + " "+ str(payload)
        print (datetime.datetime.now(), msg)
        log.error(msg)
        #raise Exception(msg)
    else:
        response= response.json()
        return response

def is_json(response):
  try:
    r = response.json()
  except ValueError as e:
    return False
  return True