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

def template_sync_status(device):
    template_sync_url = f"vnms/template/deviceGroup/deviceStatus"

    payload = {
        "versanms.deviceGroups": {
            "deviceGroupDataList": [
            {
                "name": device
            }
            ],
        "template-name": device
        }
    }

    template_sync_res = requests.post(
        url=f"{base_url}{template_sync_url}", headers=headers, auth=(user, password), data=json.dumps(payload)).json()
    
    #print(json.dumps(template_sync_res, indent=2))
    template_sync_out = template_sync_res['versanms.deviceGroups']['deviceGroupDataList']
    return template_sync_out

test = template_sync_status("test2-client")
test2 = test[0]['deviceDataList']

print(json.dumps(test2, indent=2))