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

def add_service_temp(device,site_id,org):
    service_template_url = f"vnms/sdwan/workflow/devices/device/{device}"

    payload = {
        "versanms.sdwan-device-workflow": {
            "deviceName": device,
            "siteId": site_id,
            "orgName": org,
            "serialNumber": device,
            "deviceGroup": device,
            "deviceSpecificServiceTemplates": [
            {
                "organization": "Client",
                "category": "general",
                "name": "Client_Standard_Config"
            },
            {
                "organization": "Client",
                "category": "application Steering",
                "name": "Client-Default-Application"
            },
            {
                "organization": "Client",
                "category": "qoS",
                "name": "Client-10M-qos-test"
            },
            {
                "organization": "Client",
                "category": "general",
                "name": "Client_bionic_upgrade"
            }
            ]
        }
    }

    service_template_response = requests.put(
        url=f"{base_url}{service_template_url}", headers=headers, auth=(user, password), data=json.dumps(payload), verify=False)
    
    #print(service_template_response.text)
    return service_template_response

test = add_service_temp("test2-client",119,"Client")