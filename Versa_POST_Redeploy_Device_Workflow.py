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

def redeploy_device_workflow(device):
    redeploy_dev_workflow_url = f"vnms/sdwan/workflow/devices/device/deploy/{device}"

    payload = ""

    redeploy_dev_workflow_res = requests.post(
        url=f"{base_url}{redeploy_dev_workflow_url}", headers=headers, auth=(user, password), data=payload, verify=False)
    
    #print(service_template_response.text)
    return redeploy_dev_workflow_res