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

def commit_template(device):
    commit_template_url = f"vnms/template/applyTemplate/{device}/devices"

    payload = {
        "versanms.templateRequest": {
            "device-list": [
            device
            ],
            "mode": "merge"
        }
    }

    commit_template_res = requests.post(
        url=f"{base_url}{commit_template_url}", headers=headers, auth=(user, password), data=json.dumps(payload), verify=False)
    
    #print(service_template_response.text)
    return commit_template_res