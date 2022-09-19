from flask import Flask, json, request

# init a flash web app
app = Flask(__name__)

#validate web server from meraki
@app.route('/', methods=['GET'])
def get_validator():
    return '160252c1d9fd0973c2eecb7a41b7adb44b65639b'

def get_cmxJSON():
    cmxdata = request.json

    #Detemine device type
# NOT COMPLETE