import requests
import json
from time import sleep
from side_by_side import print_side_by_side
from Dependencies import *

base_url = dep_base_url

user = dep_versa_user
password = dep_versa_pass

headers = {
    "Accept" : "application/json",
    "Content-Type" : "application/json"
}

backoffs = {
    "wait" : 60,
    "success_wait" : 390,
    "max_tries" : 180
}

osspack = {
    "wait" : 60,
    "max_tries" : 20
}

webhook = "https://test.webhook.office.com/webhookb2"

print("Enter device name:")
target_device = input()

# Get OSSPack from Director
osspack_before = get_osspack(target_device)

# Get Workflow Device Template.
device_workflow_template = get_workflow_device(target_device)
site_id = device_workflow_template['siteId']
org = device_workflow_template['orgName']

# Save service template list to roll back.
service_template_before = device_workflow_template['deviceSpecificServiceTemplates']

# Get Health from Director
def get_health(device):
    health_monitor_url = f"vnms/dashboard/appliance/{device}/live?command=orgs/org/{org}/kpi"

    health_monitor_response = requests.get(
        url=f"{base_url}{health_monitor_url}", headers=headers, auth=(user, password)).json()
    
    #print(json.dumps(health_monitor_response, indent=2))
    health_out = health_monitor_response['collection']['org:kpi'][0]
    return health_out


# Get Alerts from Director
def get_alerts(device):

    recent_monitor_url = f"vnms/fault/alarms/summary/device/{device}?org={org}&includeSystem=true"

    recent_monitor_response = requests.get(
        url=f"{base_url}{recent_monitor_url}", headers=headers, auth=(user, password)).json()
    
    #print(json.dumps(recent_monitor_response, indent=2))
    alerts_out = recent_monitor_response['List']['value']
    return alerts_out


# Add Bionic upgrade service template.
def add_service_temp(device,site_id,org):
    service_template_url = f"vnms/sdwan/workflow/devices/device/{device}"

    bionic_service = {
                "organization": org,
                "category": "general",
                "name": f"{org}_bionic_upgrade"
            }
    
    service_template = service_template_before
    service_template.append(bionic_service)
    
    payload = {
        "versanms.sdwan-device-workflow": {
            "deviceName": device,
            "siteId": site_id,
            "orgName": org,
            "serialNumber": device,
            "deviceGroup": device,
            "deviceSpecificServiceTemplates": service_template
        }
    }

    service_template_response = requests.put(
        url=f"{base_url}{service_template_url}", headers=headers, auth=(user, password), data=json.dumps(payload))
    
    #print(service_template_response.text)
    return service_template_response


# Remove Bionic upgrade service template.
def remove_service_temp(device,site_id,org):
    service_template_url = f"vnms/sdwan/workflow/devices/device/{device}"

    bionic_service = {
                "organization": org,
                "category": "general",
                "name": f"{org}_bionic_upgrade"
            }
    
    service_template = service_template_before
    service_template.remove(bionic_service)
    
    payload = {
        "versanms.sdwan-device-workflow": {
            "deviceName": device,
            "siteId": site_id,
            "orgName": org,
            "serialNumber": device,
            "deviceGroup": device,
            "deviceSpecificServiceTemplates": service_template
        }
    }

    service_template_response = requests.put(
        url=f"{base_url}{service_template_url}", headers=headers, auth=(user, password), data=json.dumps(payload))
    
    #print(service_template_response.text)
    return service_template_response


# Send Success to Teams Channel.
def Send_Teams_Success(device):
    
    payload = {
    "type":"message",
    "attachments":[
        {
            "contentType":"application/vnd.microsoft.card.adaptive",
            "contentUrl":"null",
            "content":{
                "$schema":"http://adaptivecards.io/schemas/adaptive-card.json",
                "type":"AdaptiveCard",
                "version":"1.2",
                "body":[
                    {
                    "type": "TextBlock",
                    "text": f"Wow, this is definitely a surprise."
                    },
                    {
                    "type": "TextBlock",
                    "text": f"**{device}** Upgraded successfully."
                    },
                    {
                    "type": "TextBlock",
                    "text": f"**Health Status:**"
                    },
                    {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "num-interfaces-up:"
                                }
                            ]
                        },
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                            "type": "TextBlock",
                            "text": f"{health_after['num-interfaces-up']}",
                            "color": "good"
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "num-interfaces-disabled:"
                                }
                            ]
                        },
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": f"{health_after['num-interfaces-disabled']}",
                                    "color": "attention"
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "num-interfaces-down:"
                                }
                            ]
                        },
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": f"{health_after['num-interfaces-down']}",
                                    "color": "attention"
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "num-ike-up:"
                                }
                            ]
                        },
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": f"{health_after['num-ike-up']}",
                                    "color": "good"
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "num-ike-down:"
                                }
                            ]
                        },
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": f"{health_after['num-ike-down']}",
                                    "color": "attention"
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "num-sdwan-datapath-up:"
                                }
                            ]
                        },
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": f"{health_after['num-sdwan-datapath-up']}",
                                    "color": "good"
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "num-sdwan-datapath-down:"
                                }
                            ]
                        },
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": f"{health_after['num-sdwan-datapath-down']}",
                                    "color": "attention"
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "num-bgp-up:"
                                }
                            ]
                        },
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": f"{health_after['num-bgp-up']}",
                                    "color": "good"
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "num-bgp-down:"
                                }
                            ]
                        },
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": f"{health_after['num-bgp-down']}",
                                    "color": "attention"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }
]
}

    send_post = requests.post(url=f"{webhook}", data=json.dumps(payload)).json()


# Actions:
# 1. Check basic health stats, e.g. reachablity, bgp, tunnels, etc.
# 2. Verify director config sync on templates; needs to be IN-Sync
# 3. Install trusty OSSpack - versa-flexvnf-osspack-20230629-trusty.bin
# 4. Apply bionic upgrade service template based on org
# 5. Upgrade to Bionic (manual)
# 6. Check basic health stats, e.g. reachablity, bgp, tunnels, etc.
# 7. Verify director config sync on templates; needs to be IN-Sync
# 8. Install bionic OSSpack - versa-flexvnf-osspack-20230629-bionic.bin
# 9. Remove webuser from device config.
# 10. Remove bionic upgrade service template based on org has context menu


# 1. Check basic health stats, e.g. reachablity, bgp, tunnels, etc.:

print (f"Verifying {target_device} health:\n")
# Health pre-upgrade
health_before = get_health(target_device)
print(f"\n-----\nDevice Healh\n-----\n{json.dumps(health_before, indent=2)}\n")

# Alerts pre-upgrade
alerts_before = get_alerts(target_device)
print(f"\n-----\nDevice Alerts\n-----\n{json.dumps(alerts_before, indent=2)}\n")

# Version pre-upgrade
version_before = get_version(target_device)
version = get_version(target_device)
print(f"\n-----\nDevice Package Info\n-----\n{json.dumps(version, indent=2)}\n")


# 2. Verify director config sync on templates; needs to be IN-Sync:

in_sync = False
while in_sync == False:
    print (f"Verifying {target_device} template Sync status:\n")

    template_sync = template_sync_status(target_device)
    template_state = template_sync[0]['deviceDataList'][0]['status']
    appliance_state = template_sync[0]['deviceDataList'][0]['syncStatus']

    print (f"\n{target_device} Sync Status:\n"
        f"\nTemplate State: {template_state}\n"
        f"Appliance State: {appliance_state}\n")

    # Check if device template is IN_SYNC.
    if template_state == "IN_SYNC" and appliance_state == "IN_SYNC":
        print(f"{target_device} template in sync. Proceeding to next step\n")
        in_sync = True
    else:
        print(f"\n{target_device} template not in Sync. Please correct and press Enter to continue...\n")
        input()



# 3. Install trusty OSSpack - versa-flexvnf-osspack-20230629-trusty.bin

os = "trusty"
# Check for OSSPack version before upgrade.
try:
    if osspack_before >= 20230629:
        print(f"\n---------------------------\n{target_device} OSSPack version: {osspack_before}\n---------------------------\n"
                "\nProceeding with upgrade...\n")
    else:
        print(f"\n---------------------------\n{target_device} OSSPack version: {osspack_before}\n---------------------------\n"
            f"\nUpgrading OSSPack to {os} version 20230629...\n")
        osspack_resp_code = 0
        install_osspack(target_device,os)
        while osspack_resp_code != -2:
            osspack_version = get_osspack(target_device)
            osspack_tries = 0
            if osspack_tries < osspack["max_tries"]:
                try:
                    if osspack_version == 20230629:
                        print("OSSPack upgrade completed")
                        osspack_resp_code = -2
                    else:
                        sleep(osspack["wait"])
                        print ("\nWaiting for install to finish...\n")
                        osspack_tries += 1
                except:
                    sleep(osspack["wait"])
                    print ("\nWaiting for install to finish...\n")
                    osspack_tries += 1
            else:
                print ("\nOSSPack install can't be completed. Please verify OSSPack Installation before proceeding\n")    
except:
    print(f"\n---------------------------\n{target_device} OSSPack version: {osspack_before}\n---------------------------\n"
            f"\nUpgrading OSSPack to {os} version 20230629...\n")
    osspack_resp_code = 0
    osspack_tries = 0
    install_osspack(target_device,os)
    while osspack_resp_code != -2:
        osspack_version = get_osspack(target_device)
        if osspack_tries < osspack["max_tries"]:
            try:
                if osspack_version == 20230629:
                    print("\nOSSPack upgrade completed\n")
                    osspack_resp_code = -2
                else:
                    sleep(osspack["wait"])
                    print ("\nWaiting for install to finish...\n")
                    osspack_tries += 1
            except:
                sleep(osspack["wait"])
                print ("\nWaiting for install to finish...\n")
                osspack_tries += 1
        else:
            print ("\nOSSPack install can't be completed. Please verify OSSPack installation before proceeding\n")
            exit()


# 4. Apply bionic upgrade service template based on org
            
for serv in service_template_before:
    if serv['name'] == f"{org}_bionic_upgrade":
        print (f"\n{org}_bionic_upgrade Service Template already added.\nContinue upgrade...\n")
        break
    elif service_template_before.index(serv) == len(service_template_before) -1:
        print(f"\n{org}_bionic_upgrade Template not found.\n\nAdding Bionic Service Template...")
        add_service_temp(target_device,site_id,org)
        redeploy_device_workflow(target_device)
        commit_template(target_device)
        break


# 5. Upgrade to Bionic (manual)
    
print("\nPlease proceed to upgrade the device using Versa Orchestrator.\n \nOnce the upgrade process is running return to this screen and press Enter...\n")
input()
print("\nStarting upgrade validation...\n")

# 6. Check basic health stats, e.g. reachablity, bgp, tunnels, etc.

tries = 0
resp_code = 0
health_after = ""
alerts_after = ""

# Logic to handle verification.
while resp_code != -1:        
    if tries <= backoffs["max_tries"]:
        try:
            if version['branch'] == "21.2.3" and version['os_version'] == 'bionic':
                print("\n\nFinalizing Upgrade...\n\n")
                sleep(backoffs["success_wait"])
                print("\n------------------------\nUpgrade completed\n------------------------\n")
                health_after = get_health(target_device)
                alerts_after = get_alerts(target_device)
                print_side_by_side(f"\n-----\nBefore\n-----\n"f"{json.dumps(health_before, indent=2)}", f"\n-----\nAfter\n-----\n{json.dumps(health_after, indent=2)}")
                print_side_by_side(f"\n-----\nBefore\n-----\n"f"{json.dumps(alerts_before, indent=2)}", f"\n-----\nAfter\n-----\n{json.dumps(alerts_after, indent=2)}")
                print_side_by_side(f"\n-----\nBefore\n-----\n"f"{json.dumps(version_before, indent=2)}", f"\n-----\nAfter\n-----\n{json.dumps(version, indent=2)}")
                Send_Teams_Success(target_device)
                resp_code = -1

            else:
                sleep (backoffs["wait"])
                version = get_version(target_device)
                tries += 1
                print(f"\n-----\n{tries} minutes since start\n-----\n")

        except:
            sleep (backoffs["wait"])
            tries += 1
            print(f"\n----------\n{tries} minutes since start\n----------")
            print("Device unreacheable.\n")
            pass
        
    else:
        try:
            version = get_version(target_device)
        except:
            print("Too many tries, something went wrong")
            resp_code = -1
            exit()



# 7. Verify director config sync on templates; needs to be IN-Sync

in_sync = False
while in_sync == False:
    print (f"Verifying {target_device} template Sync status:\n")

    template_sync = template_sync_status(target_device)
    template_state = template_sync[0]['deviceDataList'][0]['status']
    appliance_state = template_sync[0]['deviceDataList'][0]['syncStatus']

    print (f"\n{target_device} Sync Status:\n"
        f"\nTemplate State: {template_state}\n"
        f"Appliance State: {appliance_state}\n")

    # Check if device template is IN_SYNC.
    if template_state == "IN_SYNC" and appliance_state == "IN_SYNC":
        print(f"{target_device} template in sync. Proceeding to next step\n")
        in_sync = True
    else:
        print(f"\n{target_device} template not in Sync. Please correct and press Enter to continue...\n")
        input()


# 8. Install bionic OSSpack - versa-flexvnf-osspack-20230629-bionic.bin

osspack_after = get_osspack(target_device)
os = "bionic"
# Check for OSSPack version after upgrade.
try:
    if osspack_after >= 20230629:
        print(f"\n---------------------------\n{target_device} OSSPack version: {osspack_before}\n---------------------------\n"
                "\nProceeding with upgrade...\n")
    else:
        print(f"\n---------------------------\n{target_device} OSSPack version: {osspack_before}\n---------------------------\n"
            f"\nUpgrading OSSPack to {os} version 20230629...\n")
        osspack_resp_code = 0
        install_osspack(target_device,os)
        while osspack_resp_code != -2:
            osspack_version = get_osspack(target_device)
            osspack_tries = 0
            if osspack_tries < osspack["max_tries"]:
                try:
                    if osspack_version == 20230629:
                        print("OSSPack upgrade completed")
                        osspack_resp_code = -2
                    else:
                        sleep(osspack["wait"])
                        print ("\nWaiting for install to finish...\n")
                        osspack_tries += 1
                except:
                    sleep(osspack["wait"])
                    print ("\nWaiting for install to finish...\n")
                    osspack_tries += 1
            else:
                print ("\nOSSPack install can't be completed. Please verify OSSPack Installation before proceeding\n")    
except:
    print(f"\n---------------------------\n{target_device} OSSPack version: {osspack_before}\n---------------------------\n"
            f"\nUpgrading OSSPack to {os} version 20230629...\n")
    osspack_resp_code = 0
    osspack_tries = 0
    install_osspack(target_device,os)
    while osspack_resp_code != -2:
        osspack_version = get_osspack(target_device)
        if osspack_tries < osspack["max_tries"]:
            try:
                if osspack_version == 20230629:
                    print("\nOSSPack upgrade completed\n")
                    osspack_resp_code = -2
                else:
                    sleep(osspack["wait"])
                    print ("\nWaiting for install to finish...\n")
                    osspack_tries += 1
            except:
                sleep(osspack["wait"])
                print ("\nWaiting for install to finish...\n")
                osspack_tries += 1
        else:
            print ("\nOSSPack install can't be completed. Please verify OSSPack installation before proceeding\n")
            exit()


# 10. Remove bionic upgrade service template based on org has context menu
            
try:
    remove_service_temp(target_device,site_id,org)
    redeploy_device_workflow(target_device)
    commit_template(target_device)
    print("\nBionic Service Template removed\n"
          "\nUpgrade completed successfully\n")

except:
    print("\nTemplate not present. Upgrade completed successfully\n")