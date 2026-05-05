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

def get_osspack(device):
    osspack_url = f"vnms/appliance/applianceByName?name={device}&offset=0&limit=1"

    osspack_response = requests.get(
        url=f"{base_url}{osspack_url}", headers=headers, auth=(user, password), verify=False).json()
    
    #print(json.dumps(osspack_response, indent=2))
    try:
        osspack_out = int(osspack_response['appliances'][0]['OssPack']['osspackVersion'])
    except:
        osspack_out = osspack_response['appliances'][0]['OssPack']['osspackVersion']
    #print(osspack_out)
    return osspack_out


test = get_osspack("test2-client")


#print(json.dumps(test, indent=2))
print(test)