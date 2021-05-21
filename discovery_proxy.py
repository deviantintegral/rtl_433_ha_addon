#!/usr/bin/with-contenv python

import paho.mqtt.client as mqtt
import json
import os
import sys
from requests import get

#  function
def connect_msg():
    print('Connected to Broker')

# function
def publish_msg():
    print('Message Published')

def on_msg(client, userdata, message):
    if message.topic == "rtl_433/local-rtl-433/events":
        decoded = json.loads(message.payload)
        discovery_topic = "homeassistant/sensor/" + str(decoded["id"]) + "/config"
        discovery_payload = {
          'name': '',
          'device': {
            'identifiers': decoded["id"],
            'model': decoded["model"]
          },
          'expire_after': 60 * 60 * 3,
          'force_update': True,
          'name': decoded["model"] + " " + str(decoded["id"]),
          'state_topic': 'rtl_433/local-rtl-433/devices/' + decoded["model"] + '/0/' + str(decoded["id"]) + '/temperature_C',
          'device_class': 'temperature',
          'unit_of_measurement': "°C",
          'unique_id': decoded["model"] + '-' + str(decoded["id"])
        }

        client.publish(discovery_topic, json.dumps(discovery_payload))


# Creating client
client = mqtt.Client()

# Connecting callback functions
#client.on_connect = connect_msg
#client.on_publish = publish_msg

# Connect to broker

supervisor_token = os.environ['SUPERVISOR_TOKEN']
base_uri = "http://supervisor"
headers = {
    "Authorization": "Bearer " + supervisor_token,
    "Content-Type": "application/json",
}

mqtt_response = get(base_uri + "/services/mqtt", headers=headers)
if (mqtt_response.status_code != 200):
    # print("Unable to fetch mqtt configuration. Is the addon running?")
    sys.exit(1)

mqtt_info = mqtt_response.json()["data"]
client.username_pw_set(mqtt_info["username"], mqtt_info["password"])
client.connect(mqtt_info["host"], mqtt_info["port"])

ret = client.subscribe('rtl_433/#')
client.on_message = on_msg

# Run a loop
while True:
    client.loop()
