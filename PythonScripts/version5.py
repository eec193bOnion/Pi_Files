## NOTE: AWS cli credentials must be set up before running this script.
##       This code uses lower level client type boto3 commands.
import boto3
import os
from picamera  import PiCamera
import time
from time import sleep

## structural imports:
from firebaseAlpha import send_topic_push
from bucketFunctions import upload_files, download_file, detect_labels, clean_bucket
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
        applyMask(impath + "image1.jpg", maskpath + "mask.jpg")
        print("The mask was applied to " + impath)
    else:
        #there is no mask uploaded to the bucket
        print("No Mask Exists in the bucket: " + bucket)
        print("Applying locally stored mask to picture image1.jpg")
        applyMask(impath + "image1.jpg", maskpath + "mask.jpg")
        print("The mask was applied to " + impath)

    #upload ProcessedImage.jpg specifically to bucket
    upload_files(bucket, impath)

    #create 'labels_file' to hold all labels,
    #w+ write mode to allow overwrites and reading.
    #file is created in the ./textfiles folder
    labels_file=open(workpath + "/textfiles/labels_file.txt","w+")

    label_object_group=detect_labels('ProcessedImage.jpg',bucket)
    for label_object in label_object_group:
        labels_file.write(label_object['Name'] + "\n")

    #close file
    labels_file.close()

    #upload labels_file to s3
    upload_files(bucket, textpath)

    #begin checking labels against app-user submitted list
    download_file(bucket, "searchList.txt")
    print("downloaded searchList.txt from the bucket")

    #check for similar elements between searchList.txt and labels_file.txt
    with open(workpath + "/textfiles/labels_file.txt") as file:
        labels_list = [line.rstrip().lower() for line in file]

    with open(workpath + "/search/searchList.txt") as file:
        search_list = [line.rstrip() for line in file]

    print("Labels List:")
    print(labels_list)
    print("Search List:")
    print(search_list)

    match_list = set(labels_list).intersection(search_list)
    print("Intersection List:")
    print(match_list)
    
    #for item in match_list:
    title = "Alert: " + str(match_list).replace("{","").replace("}","").replace("'","")
    body = "A " + str(match_list).replace("{","").replace("}","").replace("'","") + " was found in your pool!"
    send_topic_push(title, body)

if __name__ == "__main__":
    main()
