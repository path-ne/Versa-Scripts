import requests
import json
from Dependencies import dep_versa_user, dep_versa_pass, dep_base_url

base_url = dep_base_url

user = dep_versa_user
password = dep_versa_pass

headers = {
    "Accept" : "application/json",
    "Content-Type" : "application/json"
}

def get_health(device):
    health_monitor_url = f"vnms/dashboard/appliance/{device}/live?command=orgs/org/Enterprise/kpi"

    health_monitor_response = requests.get(
        url=f"{base_url}{health_monitor_url}", headers=headers, auth=(user, password), verify=False).json()
    
    #print(json.dumps(health_monitor_response, indent=2))
    health_out = health_monitor_response['collection']['org:kpi'][0]
    #print(health_out)
    return health_out


test = get_health("test1-sdwan")


print(json.dumps(test, indent=2))