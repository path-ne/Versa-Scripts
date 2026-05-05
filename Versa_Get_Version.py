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

def get_version(device):

    version_monitor_url = f"vnms/dashboard/appliance/{device}/live?command=system/package-info"

    version_monitor_response = requests.get(
        url=f"{base_url}{version_monitor_url}", headers=headers, auth=(user, password), verify=False).json()

    #print(json.dumps(recent_monitor_response, indent=2))
    version_out = version_monitor_response['collection']['system:package-info'][0]
    #print(version_out)
    return version_out

test = get_version("test1-sdwan")

print(json.dumps(test, indent=2))

# if test == "21.1.2":
#     print('Success')

# else:
#     print("no good")