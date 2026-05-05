import requests
import json

dep_versa_user = "svc_versauto"
dep_versa_pass = "password"
dep_base_url = "https://sdwan.test.cloud:9182/"

user = dep_versa_user
password = dep_versa_pass
base_url = dep_base_url

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


# Get OSSPack from Director
def get_osspack(device):
    osspack_url = f"vnms/appliance/applianceByName?name={device}&offset=0&limit=1"

    osspack_response = requests.get(
        url=f"{base_url}{osspack_url}", headers=headers, auth=(user, password)).json()
    
    #print(json.dumps(osspack_response, indent=2))
    try:
        osspack_out = int(osspack_response['appliances'][0]['OssPack']['osspackVersion'])
    except:
        osspack_out = osspack_response['appliances'][0]['OssPack']['osspackVersion']
    return osspack_out


# Install OSSPACK Trusty
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
        url=f"{base_url}{install_osspack_url}", headers=headers, auth=(user, password), data=json.dumps(payload))
    
    #print(service_template_response.text)
    return install_osspack_res


# Get Workflow Device Template.
def get_workflow_device(device):
    workflow_device_url = f"vnms/sdwan/workflow/devices/device/{device}"

    workflow_device_response = requests.get(
        url=f"{base_url}{workflow_device_url}", headers=headers, auth=(user, password)).json()
    
    #print(json.dumps(workflow_device_response, indent=2))
    workflow_device_out = workflow_device_response['versanms.sdwan-device-workflow']
    return workflow_device_out


#Redeploy Device Workflow Template
def redeploy_device_workflow(device):
    redeploy_dev_workflow_url = f"vnms/sdwan/workflow/devices/device/deploy/{device}"

    payload = ""

    redeploy_dev_workflow_res = requests.post(
        url=f"{base_url}{redeploy_dev_workflow_url}", headers=headers, auth=(user, password), data=payload)
    
    #print(service_template_response.text)
    return redeploy_dev_workflow_res


# Commit template to device
def commit_template(device):
    commit_template_url = f"vnms/template/applyTemplate/{device}/devices"

    payload = {
        "versanms.templateRequest": {
            "device-list": [
            device],
            "mode": "merge"
        }
    }

    commit_template_res = requests.post(
        url=f"{base_url}{commit_template_url}", headers=headers, auth=(user, password), data=json.dumps(payload))
    
    #print(service_template_response.text)
    return commit_template_res


# Get Version from Director
def get_version(device):

    version_monitor_url = f"vnms/dashboard/appliance/{device}/live?command=system/package-info"

    version_monitor_response = requests.get(
        url=f"{base_url}{version_monitor_url}", headers=headers, auth=(user, password)).json()

    #print(json.dumps(recent_monitor_response, indent=2))
    version_out = version_monitor_response['collection']['system:package-info'][0]
    return version_out