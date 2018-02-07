import cv2
import sys
from gpiozero import MotionSensor
from picamera import PiCamera
import time
from datetime import datetime
import glob
import shutil
import os
from pubnub import Pubnub
import json

# Get user supplied values
cascPath = sys.argv[1]

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

pir = MotionSensor(6)

#captured photo name
iname=1

# use this to create a PubNub object with your publish and subscribe keys
pubnub = Pubnub(publish_key='pub-c-64f02401-e3e9-4e9d-9842-209923bfd371', subscribe_key='sub-c-815f5228-b2f0-11e6-9ab5-0619f8945a4f')

# this is the channel where you will publish the message
channel = 'motion_detection'

#Pubnub Arrays
array = {'1': 'kkk', '2' : 'kkk', '3' : 'kkk', '4' : 'kkk'}
arrayData = ""

while True:

	camera = PiCamera()
	
	#MotionSensor - wait for motion
	pir.wait_for_motion()
	
	#pi camera capture and naming
	myname=str(iname)+".jpg"
	camera.capture(myname)
	camera.close()
	time.sleep(4)
	iname+=1
	print("Recording...")
	
	#Pubnub collect data
	array[str(1)] = 'Recording...'
	
	# Read the image
	image = cv2.imread(myname)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Detect faces in the image
	faces = faceCascade.detectMultiScale(
    	gray,
    	scaleFactor=1.1,
    	minNeighbors=5,
    	minSize=(30, 30),
    	flags = 0
	)

	print("Found {0} faces!".format(len(faces)))
	
	#Pubnub collect data
	array[str(2)] = 'Found {0} faces!'.format(len(faces))
	
	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
	
	#Copy files to show in the gallery 
	src_dir = "/var/www/html/FaceDetect"
	dst_dir = "/var/www/html/FaceDetect/camFootage"
	for jpgfile in glob.iglob(os.path.join(src_dir, "*.jpg")):
		shutil.copy2(jpgfile, dst_dir)
	
	#MotionSensor - wait for no motion
	pir.wait_for_no_motion()
	time.sleep(5)
	print("Object has been recorded...")
	
	#Pubnub collect data
	array[str(3)] = 'Object has been recorded...'
	array[str(4)] = myname

	#Pubnub Publish
	arrayData = json.dumps(array)
	
	def callback(m):
		print(m)
	# Publish data to a channel using pubnub
	pubnub.publish(channel, arrayData, callback=callback, error=callback)
