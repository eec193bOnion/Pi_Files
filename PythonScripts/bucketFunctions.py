import os 
import boto3

#only downloads to the /Search/ file in the working directory at the moment
#downloads specified key from a specified bucket's /public folder
def download_file(bucket, download_key):

    #specify client
    client = boto3.client('s3', region_name='us-west-2')

    #specity working directory
    workingDirectory = os.path.dirname(os.path.abspath(__file__))

    download_to_name = download_key
    download_key = "public/" + download_key

    download_to_folder = workingDirectory+"/search/"+download_to_name

    client.download_file(bucket, download_key, download_to_folder)


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
            #uploads to the Public/ folder in the bucket
            client.upload_file(upload_path + entry, bucket, "public/" + entry)

    #return array list of all images uploaded
    return file_list


#function to return all 'Labels' for a single image in a bucket
def detect_labels(photo, bucket):

    #specify client
    client=boto3.client('rekognition')

    #set up http response to look for top 50 labels
    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':"public/ProcessedImage.jpg"}},MaxLabels=30)

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

