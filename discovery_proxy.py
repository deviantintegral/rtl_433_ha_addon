#!/usr/bin/with-contenv python

import paho.mqtt.client as mqtt
import json

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
client.username_pw_set("TBD", "TBD")
client.connect("homeassistant.lan", 1883)

ret = client.subscribe('rtl_433/#')
client.on_message = on_msg

# Run a loop
while True:
    client.loop()
