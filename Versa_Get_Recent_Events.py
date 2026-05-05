import requests
import json
from side_by_side import print_side_by_side
from Dependencies import dep_versa_user, dep_versa_pass, dep_base_url

base_url = dep_base_url

user = dep_versa_user
password = dep_versa_pass

headers = {
    "Accept" : "application/json",
    "Content-Type" : "application/json"
}

def get_alerts(device):

    recent_monitor_url = f"vnms/fault/alarms/summary/device/{device}?org=Enterprise&includeSystem=true"

    recent_monitor_response = requests.get(
        url=f"{base_url}{recent_monitor_url}", headers=headers, auth=(user, password), verify=False).json()
    
    #print(json.dumps(recent_monitor_response, indent=2))
    alerts_out = recent_monitor_response['List']['value']
    #print (alerts_out)
    return alerts_out

test = get_alerts("test1-sdwan")


#print(json.dumps(test, indent=2))

print_side_by_side(f"Before\n{json.dumps(test, indent=2)}", f"After\n{json.dumps(test, indent=2)}")
print_side_by_side(f"Before\n{json.dumps(test, indent=2)}", f"After\n{json.dumps(test, indent=2)}")