from tkinter.tix import Tree
import requests
from requests.auth import HTTPBasicAuth
from auth_token import get_token
from request_info import NetworkObjectInfo
from request_info import DeploymentInfo
import sys
import environment_info

requests.packages.urllib3.disable_warnings()

class FDM_API:

    def __init__(self, host, username, password, ):
        """ Initialize FDM/FTD API object """

        self.base_url = f"https://{host}/api"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.domainuuid = ''
        self.username = username
        self.password = password
        self.get_auth_token()

    def do_api_call (self, action, url, fdm_object = None):
        """
        Wrapper for API calls to avoid repeating code. Parameters:
        - action: HTTP verb: GET/POST/DELETE etc.
        - url: API-specific part of URL (prefixed with $base_url)
        - fdm_object: data for the POST calls
        Return: dict with the response results
        """

        api_call = requests.request(
            action,
            f"{self.base_url}/{url}",
            headers = self.headers,
            json = fdm_object,
            verify = False,
            timeout = 3,
        )
        api_call.raise_for_status()

        # debug output
        print (f" >> {action} to {api_call.url} / HTTP {api_call.status_code}")

        # HTTP 204 responses return empty output, .json() would fail with that
        if api_call.text:
            return api_call.json()

    def get_auth_token(self):
        """ Obtain authentication token and use it in future calls """

        access_token = get_token(self.username,self.password)
        self.headers['X-auth-access-token'] = f'{access_token}'
        print(self.headers)

    def deploy (self):
        """
        Call "https://{host}/api/fdm/latest/operational/deploy"
        to deploy prepared configuration changes
        """

        response = self.do_api_call("POST", f"fmc_config/v1/domain/{self.domainuuid}/deployment/deploymentrequests", DeploymentInfo)
        return True

    def get_domain_id(self):
        url = f'{self.base_url}/fmc_platform/v1/info/domain'
        data = {}
        response = requests.get(url,headers=self.headers,data=data,verify=False)
        response.raise_for_status()
        print(response.json()['items'])
        for domain in response.json()['items']:
            print(f'Found domain: {domain["name"]}')
            if domain['name'] == environment_info.LAB_FDM['domain']:
                print(f'Found the correct domain: {domain["name"]}')
                self.domainuuid = domain['uuid']
                return True
        print(f"{environment_info.LAB_FDM['domain']}: Domain not found")
        sys.exit(1)

def find_object_by_name (obj_name, obj_list):
    """
    Helper function
    Find if the object with a given "obj_name" exists in the "obj_list" list
    Return: ID of the existing object
    """

    for obj in obj_list:
        if obj_name['name'] == obj['name']:
            return obj['id']
    return None

def main():
    # Disable certificate warnings
    requests.packages.urllib3.disable_warnings()

    # Settings for the "Firepower Threat Defense REST API" DevNet sandbox

    fdm=FDM_API(environment_info.LAB_FDM["host"],environment_info.LAB_FDM['username'],environment_info.LAB_FDM['password'])

    fdm.get_domain_id()

    # read and print current network objects
    fdm_net_objs = fdm.do_api_call("GET", f"fmc_config/v1/domain/{fdm.domainuuid}/object/networks")
    for net_obj in fdm_net_objs['items']:
        print(f"Existing {net_obj['name']} object, ID:{net_obj['id']}")

    # Check if object with the same name already exists
    # if so, delete it first to avoid errors
    obj_id = find_object_by_name (NetworkObjectInfo, fdm_net_objs['items'])
    if obj_id:
        print(f"{NetworkObjectInfo['name']} object already exists, deleting...")
        fdm.do_api_call ("DELETE", f"fmc_config/v1/domain/{fdm.domainuuid}/object/networks/{obj_id}")

    # Create a new network object
    new_object = fdm.do_api_call ("POST", f"fmc_config/v1/domain/{fdm.domainuuid}/object/networks", NetworkObjectInfo)
    print(f"Created {new_object['name']} object, ID:{new_object['id']}")

    # Configuration changes need to be deployed to be activated
    # Note it will fail in the DevNet sandbox when it's Read-Only
    fdm.deploy()

if __name__ == "__main__":
    main()