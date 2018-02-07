import sys
from pubnub import Pubnub
import json

# use this to create a PubNub object with your publish and subscribe keys
pubnub = Pubnub(publish_key='pub-c-64f02401-e3e9-4e9d-9842-209923bfd371', subscribe_key='sub-c-815f5228-b2f0-11e6-9ab5-0619f8945a4f')

# this is the channel where you will publish the message
channel = 'motion_detection'

# data the you want to publish
data = {
  'username': 'Musfiq',
  'message': 'Hello World from Pi!'
}

# convert the data to a Json object
data = json.dumps(data)

# when something goes wrong, this method will be called back 
def callback(m):
  print(m)

# Publish data to a channel using pubnub
pubnub.publish(channel, data, callback=callback, error=callback)
