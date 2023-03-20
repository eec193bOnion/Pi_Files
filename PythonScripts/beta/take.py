import boto3
import os

from picamera  import PiCamera
from time import sleep

camera = PiCamera()
#camera.rotation = 180

os.chdir("/home/pi/Onion/PythonScripts/images")

camera.start_preview()
for i in range(1,5):
        sleep(3)
        camera.capture('pool%s.jpg' % i)
camera.stop_preview()
