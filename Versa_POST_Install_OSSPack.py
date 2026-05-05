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

def install_osspack(device,os):
    install_osspack_url = f"vnms/osspack/device/install-osspack"

    payload = {
        "update-type": "full",
        "version": "20230629",
        "os-version": os,
        "devices": [
            device
        ]
    }

    install_osspack_res = requests.post(
        url=f"{base_url}{install_osspack_url}", headers=headers, auth=(user, password), data=json.dumps(payload), verify=False)
    
    #print(service_template_response.text)
    return install_osspack_res

test = install_osspack("test2-client")