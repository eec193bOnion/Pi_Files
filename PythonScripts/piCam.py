import os
from picamera  import PiCamera

def camera():
    camera = PiCamera()

    #specify working directory of MAIN script
    workingDirectory = os.path.dirname(os.path.abspath(__file__))
    #specify the directory which holds all images for upload and labeling
    imageDirectory = workingDirectory + "/images/"
    #Locate Directory
    os.chdir(imageDirectory)

    #Turn on camera/starts preview
    camera.start_preview()
    camera.capture('image1.jpg')
    camera.stop_preview()


def delete():
    #specify working directory of MAIN script
    workingDirectory = os.path.dirname(os.path.abspath(__file__))
    #specify the directory which holds all images for upload and labeling
    imageDirectory = workingDirectory + "/images/"
    #Locate Directory
    os.chdir(imageDirectory)

    #Delete image if exists
    if os.path.exists(imageDirectory + "image1.jpg"):
        os.remove(imageDirectory + "image1.jpg")
    else:
        print("File does not exist.")
