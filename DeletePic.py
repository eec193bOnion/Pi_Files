import boto3
import os

os.chdir("/home/pi/Onion/PythonScripts/images")

for i in  range(1,4):
	if os.path.exists("pool%s.jpg" % i):
		os.remove("pool%s.jpg" % i)
	else:
		print("File does not exist.")

