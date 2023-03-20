import boto3
import os

os.chdir("/home/pi/Onion/PythonScripts/images")

if os.path.exists("image1.jpg"):
    os.remove("image1.jpg")
else:
    print("File does not exist.")
