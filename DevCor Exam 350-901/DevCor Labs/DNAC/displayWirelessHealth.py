import requests
from requests.auth import HTTPBasicAuth
import env_lab

requests.packages.urllib3.disable_warnings()

class DnacApi:
    def __init__(self):
        self.system_url = f"https://{env_lab.DNA_CENTER['host']}/dna/system/api/v1"
        self.intent_url = f"https://{env_lab.DNA_CENTER['host']}/dna/intent/api/v1"
        self.username = env_lab.DNA_CENTER['username']
        self.password = env_lab.DNA_CENTER['password']
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        self.headers["X-Auth-Token"] = self.get_auth_token()

    def get_auth_token(self):
        # Endpoint URL
        url =  f"{self.system_url}/auth/token"

        resp = requests.post(url, auth=HTTPBasicAuth(self.username, self.password), verify=False)

        token = resp.json()['Token']

        print("Token Retrieved: {}".format(token))

        return token

    def api_read(self,api_url):
        """ Perform "GET" DNA Center API call """

        response = requests.get(
            f"{self.intent_url}/{api_url}",
            headers=self.headers,
            verify=False
        )
        response.raise_for_status()
        return response.json()

def main():

    dnac = DnacApi()

    print("*** Network Wireless Health Status ***")
    site_health = dnac.api_read("site-health")['response']
    for site in site_health:
        if site['wirelessDeviceTotalCount']:
            print(f"Site: {site['siteName']}: \n"
                f"  Wireless Network Health: {site['networkHealthWireless']}% "
                f"({site['wirelessDeviceGoodCount']}/{site['wirelessDeviceTotalCount']} OK) \n"
                f"  Wireless Client Health: {site['clientHealthWireless']}% for {site['numberOfWirelessClients']} clients"
            )

    print("\n*** Client Wireless Health Status ***")
    client_health = dnac.api_read("client-health")['response'][0]

    for score in client_health["scoreDetail"]:
        print(
            f"Health score for {score['scoreCategory']['value']}: "
            f"{score['scoreValue']}% for {score['clientCount']} clients"
        )
        # drill down into score categories
        scorelist = score.get('scoreList',{})
        for scoreitem in scorelist:
            if scoreitem['clientCount'] > 0:        # skip empty ones
                print(
                    f"  {scoreitem['scoreCategory']['value']}"
                    f": {scoreitem['clientCount']} clients"
                )
if __name__ == "__main__":
    main()

