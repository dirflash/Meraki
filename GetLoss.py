# This script pulls the loss percentage off of the WAN interface on
# my Meraki MX68 firewall.  Your mileage may vary.

import json
import requests


keys_file = open("keys.txt")
lines = keys_file.readlines()
Meraki_API_Key = lines[0].rstrip()
LandLurl = lines[1].rstrip()
payload = ""

querystring = {
    'ip': "1.1.1.1",
    'timespan': "600",
    'resolution': "600"
}

headers = {
    'X-Cisco-Meraki-API-Key': "",
    'cache-control': "no-cache"
}

headers["X-Cisco-Meraki-API-Key"] = Meraki_API_Key

LandLresponse = requests.request(
    "GET", LandLurl, data=payload, headers=headers, params=querystring)

response_data = LandLresponse.json()

# Figure out the length of the list and define last one
list_qty = len(response_data)
last_list = len(response_data) - 1

highlighted_data = response_data[last_list]

lp = response_data[last_list]['lossPercent']
loss_percent = json.dumps(lp).replace('"', '')

print("Loss percentage for 'Lab3 MX68' is {}".format(loss_percent))
