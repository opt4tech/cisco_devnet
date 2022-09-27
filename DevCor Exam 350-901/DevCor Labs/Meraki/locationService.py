from flask import Flask, json, request, render_template
import sys, getopt
import json
from pprint import pprint
from environment_info import SANDBOX_MERAKI

# init a flash web app
app = Flask(__name__, static_url_path='/5002/static')

#validate web server from meraki
@app.route('/', methods=['GET'])

def get_validator():
    print('validator sent to: ', request.environ["REMOTE_ADDR"])
    return SANDBOX_MERAKI['validator']

@app.route("/", methods=["POST"])
def get_locationJSON():
    global locationdata

    if not request.json or not "data" in request.json:
        return ("invalid data", 400)

    locationdata = request.json

    pprint(locationdata, indent=1)
    print("Received POST from ", request.environ["REMOTE_ADDR"])

    if locationdata["secret"] != SANDBOX_MERAKI["secret"]:
        print("secret invalid: ", locationdata["secret"])
        return ("invalid secret", 403)
    
    else:
        print("secret verified", locationdata["secret"])
    
    if locationdata["version"] != SANDBOX_MERAKI["version"]:
        print("invalid version")
        return ("invalid version", 400)
    else:
        print("version verified: ", locationdata["version"])
    
    if locationdata["type"] == "DevicesSeen":
        print("WiFi Devices Seen")
    elif locationdata["type"] == "BluetoothDevicesSeen":
        print("Bluetooth Devices Seen")
    else:
        print("Unknown Device 'type'")
        return ("invalid device type", 403)

    # Return success message
    return "Location Scanning POST Received"

@app.route("/receive", methods=["GET"])
def get_go():
    return render_template("index.html", **locals())

@app.route("/clients/",)
def get_clients():
    global locationdata
    if locationdata != "Location Data Holder":
        pprint(locationdata["data"]["observations"], indent=1)
        return json.dumps(locationdata["data"]["observations"])
    return ""
    
@app.route("/clients/<clientMac>", methods=["GET"])
def get_individualclients(clientMac):
    global locationdata
    for client in locationdata["data"]["observations"]:
        if client["clientMac"] == clientMac:
            return json.dumps(client)

    return ""

def main(argv):
    global validator
    global secret
    validator = SANDBOX_MERAKI['validator']
    secret = SANDBOX_MERAKI['secret']

    try:
        opts, args = getopt.getopt(argv, "hv:s:", ["validator=", "secret="])
    except getopt.GetoptError:
        print("locationscanningreceiver.py -v <validator> -s <secret>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("locationscanningreceiver.py -v <validator> -s <secret>")
            sys.exit()
        elif opt in ("-v", "--validator"):
            validator = arg
        elif opt in ("-s", "--secret"):
            secret = arg

    print("validator: " + validator)
    print("secret: " + secret)


if __name__ == "__main__":
    main(sys.argv[1:])
    app.run(host="0.0.0.0", port=5002, debug=False)

