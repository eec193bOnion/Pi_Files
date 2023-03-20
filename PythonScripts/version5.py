## NOTE: AWS cli credentials must be set up before running this script.
##       This code uses lower level client type boto3 commands.
import boto3
import os
from picamera  import PiCamera
import time
from time import sleep

## structural imports:
from bucketFunctions import upload_files, detect_labels, clean_bucket
from maskProc import checkForMask, downloadMask, applyMask
from piCam import camera, delete
from sensors import sensor, read, loop

def main():
    ## INSERT BUCKET NAME HERE##
    bucket='truedrowningstorage170305-dev'

    #specify image and text mask path
    workpath = os.path.dirname(os.path.abspath(__file__))
    impath = workpath + "/images/"
    textpath = workpath + "/textfiles/"
    maskpath = workpath +  "/maskfiles/"

    try:
        #initialize camera preview and take a picture
        camera()

        print("Saved a new picture to ./images/image1.jpg")
    except:
        print("ERROR: No camera detected")

    #look for and apply a mask, new image saved into ./images/ProcessedImage.jpg
    if (checkForMask(bucket)):
        #mask exists under the name "mask.jpg"
        print("Mask, mask.jpg, Exists in the bucket: " + bucket)
        #download mask
        downloadMask(bucket)
        print("Mask downloaded!")

        #apply the mask
        #saves new image to the /image/ directory
        applyMask(impath + "/image1.jpg", maskpath + "/mask.jpg")
        print("The mask was applied to " + impath)
    else:
        #there is no mask uploaded to the bucket
        print("No Mask Exists in the bucket: " + bucket)
        print("Applying locally stored mask to picture image1.jpg")
        applyMask(impath + "/image1.jpg", maskpath + "/mask.jpg")
        print("The mask was applied to " + impath)

    #completely clear all files from the s3 bucket
    #try:
    #    clean_bucket(bucket)
    #except:
    #    print("empty bucket")

    #delete image1.jpg
    #delete()

    #upload ProcessedImage.jpg specifically to bucket
    upload_files(bucket, impath)

    #try:
    #    delete()
    #    print("deleted ./images/image1.jpg")
    #except:
    #    print("ERROR: No image1.jpg to delete")

    #create 'labels_file' to hold all labels,
    #w+ write mode to allow overwrites and reading.
    #file is created in the ./textfiles folder
    labels_file=open(workpath + "/textfiles/labels_file.txt","w+")

    #for every photo in 'photoArray', display image data from rekognition
    #for photo in photoArray:

        #detect labels for single image
        #label_object_group=detect_labels(photo, bucket)

        #write each label to the labels_file
        #for label_object in label_object_group:
            #labels_file.write(label_object['Name'] + "\n")

    label_object_group=detect_labels('ProcessedImage.jpg',bucket)
    for label_object in label_object_group:
        labels_file.write(label_object['Name'] + "\n")

    #close file
    labels_file.close()

    #upload labels_file to s3
    upload_files(bucket, textpath)

if __name__ == "__main__":
    main()
    #sleep(1)
