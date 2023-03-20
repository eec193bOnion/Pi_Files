#import the pathing os library
import os

#import boto3
#and some specific botocore errors for the mask checker
import boto3
import botocore
from botocore.errorfactory import ClientError

#import Pillow's image processing library
from PIL import Image, ImageMath

#import numpy to help process out the black background out
import numpy as np

#note: from now on all files will be passed into the Public file in>
def checkForMask(bucket):

        #set boto3 resource to s3
        client = boto3.client('s3', region_name='us-west-2')

        #define the mask name
        maskName = "mask.jpg"
        maskKey = "public/" + maskName

        #set mask directory to Public/ inside the bucket
        try:
                client.head_object(Bucket=bucket, Key=maskKey)

        except botocore.exceptions.ClientError as e:

                if e.response['Error']['Code'] == "404":
                        # The object does not exist.
                        print("MASK DOES NOT EXIST in the bucket - maskProc\n")
                        return 0
                else:
                        # Something else has gone wrong.
                        raise e

        else:
                # The object does exist.
                return 1


def downloadMask(bucket):
        client = boto3.client('s3', region_name='us-west-2')

        workingDirectory = os.path.dirname(os.path.abspath(__file__))

        maskName = "mask.jpg"
        maskKey = "public/" + maskName
        maskDirLocal = workingDirectory+"/maskfiles/"+maskName

        #download a file called "mask.jpg" and save it to ./maskfiles/
        client.download_file(bucket, maskKey, maskDirLocal)


def applyMask(imagePath, maskPath):

        #specify working directory of MAIN script
        workingDirectory = os.path.dirname(os.path.abspath(__file__))
        #specify the directory which holds all images for upload and labeling
        imageDirectory = workingDirectory + "/images/"

        #code from: https://www.geeksforgeeks.org/overlay-an-image-on-another-image-in-python/
        # Opening the primary image (used in background)
        im1 = Image.open(imagePath)

        # Opening the secondary image (overlay image) and converting it to RGBA
        maskDownload = Image.open(maskPath).convert('RGBA')
        data = np.array(maskDownload)
        
	#https://stackoverflow.com/questions/3752476/python-pil-replace-a-single-rgba-color
        red, green, blue, alpha = data.T
        black_areas = (red == 0) & (blue == 0) & (green == 0) & (alpha == 255)
        data[..., :][black_areas.T] = (255, 255, 255, 0)
        mask = Image.fromarray(data, mode='RGBA')
        
        r, g, b, a = maskDownload.getpixel((1,1))
        print("maskproc.py -> Downloaded Mask's top corner pixel values: ") 
        print(r, g, b, a)

        width, height = im1.size
        print(width, height)

        maskResize = mask.resize((width, height))
        
        maskWidth, maskHeight = maskResize.size
        print(maskWidth, maskHeight)

        # Pasting img2 image on top of img1
        # starting at coordinates (0, 0)
        im1.paste(maskResize, (0,0), mask = maskResize)

        im1 = im1.save(imageDirectory + "ProcessedImage.jpg")
