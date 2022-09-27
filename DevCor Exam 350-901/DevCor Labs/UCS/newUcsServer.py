import requests
import xmltodict
from parameters import NewUcsServer

class UCS_API:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.cookie = None
    def api_request(self, body):
        """
        Wrapper for API calls to avoid repeating code.
        Parameter: body is a complete XML request
        Return: dict with the response status and result
        """
        api_response = requests.post(f"http://{self.host}/nuova",
                                     headers={"Content-Type": "application/x-form-urlencoded"},
                                     data=body,
                                     )
        api_response.raise_for_status()

        status = api_response.status_code

        data = xmltodict.parse(api_response.text)
        
        return (status, data)

    def login(self):
        body = f'<aaaLogin inName="{self.username}" inPassword="{self.password}" />'

        response = self.api_request(body)
        if response[0] == 200:
            self.cookie = response[1]["aaaLogin"]["@outCookie"]
            return self.cookie
    
    def logout(self):
        body = f'<aaaLogout inCookie="{self.cookie}" />'
        self.api_request(body)

    def create_server_from_profile(self, name, template):
        body = (
            f'<configConfMo dn="" cookie="{self.cookie}">'
            f'  <inConfig>'
            f'    <lsServer dn="org-root/ls-{name}"'
            f'              name="{name}"'
            f'              srcTemplName="{template}"/>'
            f'  </inConfig>'
            f'</configConfMo>'
        )

        response = self.api_request(body)
        return response

if __name__ == "__main__":

    UCS_HOST = NewUcsServer['HOST']
    UCS_USER = NewUcsServer['USER']
    UCS_PASS = NewUcsServer['PASS']
    ucs = UCS_API(UCS_HOST, UCS_USER, UCS_PASS)

    # supply template and target instance names
    template = NewUcsServer['TEMPLATE']
    name = NewUcsServer['NAME']

    response = ucs.create_server_from_profile (name, template)

    resp_status = response[1]["configConfMo"]["outConfig"]["lsServer"].get("@status")
    if response[0] == 200 and resp_status == "created":
        print(f'The service profile {name} created successfully.')
    else:
        print(f'The service profile {name} was not created.')

    ucs.logout()

