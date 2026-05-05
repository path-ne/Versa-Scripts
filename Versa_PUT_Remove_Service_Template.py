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

def put_remove_service_temp(device,site_id,org):
    service_template_url = f"vnms/sdwan/workflow/devices/device/{device}"

    bionic_service = {
                "organization": org,
                "category": "general",
                "name": f"{org}_bionic_upgrade"
            }

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
                "category": "General",
                "name": "Client_Standard_Config"
            },
            {
                "organization": "Client",
                "category": "Application Steering",
                "name": "Client-Default-Application"
            },
            {
                "organization": "Client",
                "category": "QoS",
                "name": "Client-10M-qos-test"
            }
            ]
        }
    }

    service_template_response = requests.put(
        url=f"{base_url}{service_template_url}", headers=headers, auth=(user, password), data=json.dumps(payload), verify=False)
    
    #print(service_template_response.text)
    return service_template_response

test = put_remove_service_temp("test2-client",119,"Client")