import requests
from requests.auth import HTTPBasicAuth

def get_token(username, password):
    base_url = "https://fmcrestapisandbox.cisco.com/api"
    auth_url = f"{base_url}/fmc_platform/v1/auth/generatetoken"
    headers = {
        'Authorization': 'Basic ZWFuZ2VsZTkwOlZlTjdHRHVG',
}
    data = {}
    response = requests.post(auth_url,auth=HTTPBasicAuth(username,password),headers=headers,data=data,verify=False)
    response.raise_for_status()
    return response.headers['X-auth-access-token']

if __name__ == "__main__":
    get_token()