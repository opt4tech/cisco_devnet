from environment_info import SANDBOX_MERAKI
import requests
#import json
import logging
import sys

def do_api_call(api_url, action = "GET", json = None):
    """
    Basic wrapper for doing an api call. Parameters
    - resource - URI extention to the base URL.
    - action - GET, POST, etc.
    - json - data for PUT/POST calls
    Return: API response results
    """
    base_url = f"https://{SANDBOX_MERAKI['host']}/api/v0"
    headers = {
        'X-Cisco-Meraki-API-Key': '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'
        }

    try:
        api_call = requests.request(method=action,url=f"{base_url}/{api_url}",headers=headers,json=json,timeout=30,)
        logging.info(f" API CALL >> {action} to {api_call.url} / HTTP {api_call.status_code}")
    except Exception as e:
        logging.error(f" API CALL >> FAILED {action} to {base_url}/{api_url} failed with error: {e}")
        sys.exit(1)
    try:
        api_call.raise_for_status()
    except Exception as e:
        logging.error(f" API CALL >> FAILED {action} to {api_call.url} failed with error: {e}")
        sys.exit(1)
    if api_call.text:
        return api_call.json()

def find_network_id(org_name, net_name):
    """
    Parameters:
    - org_name: text organization name, may be partial as soon as unique
    - net_name: text network name, may be partial as soon as unique
    Return: ID of the network for API calls, or None if not found
    """
    logging.info(f"FIND NETWORK >> Searching for org id: {org_name}")

    orgs = do_api_call("organizations")

    for org in orgs:
        if org_name.lower() == org['name'].lower():
            logging.info(f"FIND NETWORK >> Found a match for the {org['name']} org")
            organizationId = org['id']
            break
    
    logging.info(f"FIND NETWORK >> Searching for network id for : {net_name}")

    if organizationId:
        nets = do_api_call(f"organizations/{organizationId}/networks")
        for net in nets:
            if net_name.lower() in net['name'].lower():
                logging.info(f"FIND NETWORK >> Found Found a match for the {net['name']} network")
                return net['id']

def find_ssid_id(net_id, ssid_name):
    """
    Parameters:
    - org_name: text organization name, may be partial as soon as unique
    - net_name: text network name, may be partial as soon as unique
    Return: ID of the network for API calls, or None if not found
    """
    logging.info(f"FIND SSID >> Searching for ssid for : {ssid_name}")
    
    ssids = do_api_call(f"/networks/{net_id}/ssids")

    for ssid in ssids:
        if ssid_name.lower() in ssid['name'].lower():
            logging.info(f"FIND SSID >> Found a match for the {ssid_name} network")
            return ssid['number']

def main():
    logging.info(f"MAIN >> Program Begins")
    
    network_id = find_network_id(SANDBOX_MERAKI['org_name'], SANDBOX_MERAKI['net_name'])

    ssid_id = find_ssid_id(network_id, SANDBOX_MERAKI['ssid_name'])

    print(ssid_id)


    

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,format='%(levelname)s: %(message)s')
    logging.getLogger("paramiko").setLevel(logging.WARNING)
    main()
