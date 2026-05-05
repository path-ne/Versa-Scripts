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

def get_workflow_device(device):
    workflow_device_url = f"vnms/sdwan/workflow/devices/device/{device}"

    workflow_device_response = requests.get(
        url=f"{base_url}{workflow_device_url}", headers=headers, auth=(user, password), verify=False).json()
    
    #print(json.dumps(workflow_device_response, indent=2))
    workflow_device_out = workflow_device_response['versanms.sdwan-device-workflow']
    #print(workflow_device_out)
    return workflow_device_out


test = get_workflow_device("test2-client")


print(json.dumps(test, indent=2))

# print(test['siteId'])
# print(test['orgName'])
# print(json.dumps(test['deviceSpecificServiceTemplates'], indent=2))
