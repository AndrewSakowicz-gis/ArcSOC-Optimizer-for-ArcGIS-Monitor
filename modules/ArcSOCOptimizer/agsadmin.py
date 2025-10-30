import requests,json, urllib

class AGSAdmin:
    def __init__(self, server_admin_url, token_url, username, password, client, referer):
        #self.token_url=token_url
        # self.username=username
        # self.password=password
        self.server_admin_url=server_admin_url
        self.token=self._get_token(token_url, username, password, client, referer)
    # def _get_token_url(self):
    #     payload = {
    #     "f":"json"
    #     }
    #     payload=urllib.parse.urlencode(payload)
    #     headers = {"Accept": "text/plain"}
        
    #     route = "/rest/info?f=json"
    #     response = requests.request("GET", self.server_admin_url + route, headers=headers, verify=False)
    #     token_url=(response.json()["authInfo"]["tokenServicesUrl"])
    #     return token_url
    def _get_token(self, token_url, username, password, client, referer):
        #url=self._get_token_url()
        #"referer":  url.removesuffix('/sharing/rest/generateToken'),
        payload = {
        "username": username,
        "password": password,
        "client": client,
        "referer":  referer,
        "f":"json",
        "expiration":120  
        }
        payload=urllib.parse.urlencode(payload)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html"}

        response = requests.request("POST", token_url, data=payload, headers=headers, verify=False)
        token=response.json()["token"]
        #print (token)
        return token
   
    def get_service(self, folderName, serviceName, serviceType):
        payload = {
            "token": self.token,
            "f":"pjson"      
        }
        headers = { "Content-Type": "application/x-www-form-urlencoded"}
        #headers = { "Content-Type": "application/x-www-form-urlencoded", "referer": self.server_admin_url}
        if folderName=="/": folderName=""
        route = "/admin/services/"+folderName+"/" + serviceName+"."+serviceType

        response = requests.request("POST", self.server_admin_url + route, data=payload, headers=headers, verify=False)

        return response
    def edit_instances(self, folderName, serviceName, serviceType, minInstancesPerNode, maxInstancesPerNode):
        serviceJson=self.get_service(folderName, serviceName, serviceType)
        serviceJson=serviceJson.json()
        serviceJson["minInstancesPerNode"]=minInstancesPerNode
        serviceJson["maxInstancesPerNode"]=maxInstancesPerNode
        serviceJson=json.dumps(serviceJson)
        payload = {
            "service":serviceJson,
            "token": self.token,
            "f":"json"      
        }
        #headers = { "Content-Type": "application/x-www-form-urlencoded", "referer": self.server_admin_url}
        headers = { "Content-Type": "application/x-www-form-urlencoded"}
        if folderName=="/": folderName=""
        route = "/admin/services/"+folderName+"/" + serviceName+"."+serviceType+"/edit"
        response = requests.request("POST", self.server_admin_url + route, data=payload, headers=headers, verify=False)

        return response

    def dedicated_to_shared(self, folder, service_name, service_type):
        return self._change_provider(folder, service_name, service_type,"DMaps" )
    def shared_to_dedicated(self, folder, service_name, service_type):
        return self._change_provider(folder, service_name, service_type,"ArcObjects11" )
    def _change_provider(self, folder, service_name, service_type, provider):
        payload = {
            "provider":provider,
            "token": self.token,
            "f":"json"      
        }
        #headers = { "Content-Type": "application/x-www-form-urlencoded", "referer": self.server_admin_url}
        headers = { "Content-Type": "application/x-www-form-urlencoded"}
        if folder=="/": folder=""
        route = "/admin/services/"+folder+"/" + service_name+"."+service_type+"/changeProvider"
        response = requests.request("POST", self.server_admin_url + route, data=payload, headers=headers, verify=False)
        
        return response