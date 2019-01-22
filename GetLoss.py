# This script pulls the loss percentage off of the WAN interface on
# my Meraki MX68 firewall.  Your mileage may vary.

# Sends status update to Twitter, using Tweepy.

import json
import requests
import tweepy

# Meraki
keys_file = open("keys.txt")
lines = keys_file.readlines()
Meraki_API_Key = lines[0].rstrip()
Meraki_Net = lines[1].rstrip()
Meraki_Device = lines[2].rstrip()
base_url = "https://api.meraki.com/api/v0/networks/"
device_url = "/devices/"
loss_url = "/lossAndLatencyHistory"

LandLurl = base_url + Meraki_Net + device_url + Meraki_Device + loss_url

# Tweepy
consumer_key = lines[3].rstrip()
consumer_secret = lines[4].rstrip()
access_token = lines[5].rstrip()
access_token_secret = lines[6].rstrip()
status_msg = "Hello Everyone! Using a bit of Python programming.  I am able to determine that the loss percentage for the WAN interace on my Meraki Lab3 MX68 is "

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

# Tweepy authentication of consumer key and secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Tweepy authentication of access token and secret
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# update the status
api.update_status(status=status_msg + "{}%.".format(loss_percent))
