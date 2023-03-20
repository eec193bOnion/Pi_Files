import boto3
import os
from picamera  import PiCamera
import time
from time import sleep

#uploads all images from the directory 'impath' to input parameter bucket
#returns a list of all images uploaded
def upload_files(bucket, upload_path):

    #initialize imageList output
    file_list = [];

    #specify client
    client = boto3.client('s3', region_name='us-west-2')

    #run client based upload for every file in the images folder
    for entry in os.listdir(upload_path):
        if os.path.isfile(os.path.join(upload_path, entry)):
            print("uploaded file from " + upload_path + " : " + entry)
            file_list.append(entry)
            client.upload_file(upload_path + entry, bucket, entry)

    #return array list of all images uploaded
    return file_list


#function to return all 'Labels' for a single image in a bucket
def detect_labels(photo, bucket):

    #specify client
    client=boto3.client('rekognition')

    #set up http response to look for top 50 labels
    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},MaxLabels=30)

    #print rekogintion data for the photo
    print()
    print('Detected labels for ' + photo)
    for label in response['Labels']:
        print ("Label: " + label['Name'])
        #print ("Confidence: " + str(label['Confidence']))

    #return 'Labels' object for single image
    return response['Labels']


def clean_bucket(bucket):

    #specify client
    client=boto3.client('s3', region_name='us-west-2')

    #for every item in list of everything in the bucket, delete file.
    response = client.list_objects_v2(Bucket=bucket)
    files = response.get("Contents")
    try:
        for file in files:
                print(f"deleted from s3: {file['Key']}, size: {file['Size']}")
                client.delete_object(Bucket=bucket, Key=file['Key'])
    except Exception:
        print("The Bucket is empty. Nothing deleted from s3")

    #return arbitrary standin value
    return 247


def main():

    a=1
    while a<5:

        camera = PiCamera()
        os.chdir("/home/pi/Onion/PythonScripts/images")

        camera.start_preview()
        sleep(2)
        camera.capture('image1.jpg')
        camera.stop_preview()


       ## INSERT BUCKET NAME HERE##
        bucket='custom-labels-console-us-west-2-273838cf31'

        #completely clear all files from the s3 bucket
        try:
            clean_bucket(bucket)
        except:
            print("empty bucket")

        #upload all images and save list of uploaded image names to 'photoArray'
        #specify image path
        workpath = os.path.dirname(os.path.abspath(__file__))
        impath = workpath + "/images/"
        photoArray=upload_files(bucket, impath)

        os.chdir("/home/pi/Onion/PythonScripts/images")

        if os.path.exists("image1.jpg"):
            #os.remove("image1.jpg")
            print("Hellllllllllllllllllll")
        else:
            print("File does not exist.")

        #create 'labels_file' to hold all labels,
        #w+ write mode to allow overwrites and reading.
        #file is created in the ./textfiles folder
        labels_file=open(workpath + "/textfiles/labels_file.txt","w+")

        print("This will be loop number%s" %a)
        a=a+1

        #for every photo in 'photoArray', display image data from rekognition
        for photo in photoArray:

            #detect labels for single image
            label_object_group=detect_labels(photo, bucket)
         #write each label to the labels_file
            for label_object in label_object_group:
                labels_file.write(label_object['Name'] + "\n")

        #close file
    labels_file.close()

        #upload labels_file to s3
    textpath = workpath + "/textfiles/"
    upload_files(bucket, textpath)


if __name__ == "__main__":
    while True:
        main()
       # time.sleep(5)
