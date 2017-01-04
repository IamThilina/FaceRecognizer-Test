#!/usr/bin/python

# Import the required modules
import cv2, os
import numpy as np
import urllib, cStringIO
from PIL import Image

IMAGE_SIZE = 100 # image size of training and testing data
DISPLAY_IMAGE_SIZE = 100 # image size of displaying windows
ORIGINAL_IMAGE_RESIZE = 500 # resize original images to this size
GOV_MIN_FACE_SIZE = 300 # minimum object size for government images
SOCIAL_MEDIA_MIN_FACE_SIZE = 80 # minimum object size for social media images

# Path to the DataSets
socialMediaDataSetPath = '../resources/social_media_faces'
governmentDataSetPath = '../resources/government_faces'

# For face detection we will use the Haar Cascade provided by OpenCV.
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# For face recognition we will the the LBPH Face Recognizer
recognizer = cv2.createLBPHFaceRecognizer(1,8,8,8)

#######
'''
URL = 'http://localhost:3000/images/test.jpg'
file = cStringIO.StringIO(urllib.urlopen(URL).read())
img = Image.open(file)
cv2.imshow("Testing URL Image", np.array(img, 'uint8'))
cv2.waitKey(0)
'''
#######

def detectGovernmentFaces(profileList):

    # Append all the absolute image paths in a list image_paths
    #image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    count = 0

    #for image_path in image_paths:
    for profile in profileList:

        # Read the image and convert to grayscale
        URL = profile['NIC data']['picture']
        image_path = cStringIO.StringIO(urllib.urlopen(URL).read())
        image_pil = Image.open(image_path).convert('L')
        # Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')
        # resize the images
        #cv2.resize(image, (ORIGINAL_IMAGE_RESIZE,ORIGINAL_IMAGE_RESIZE))
        # Detect the face in the image, consider the object larger than size(1000,1000)
        faces = faceCascade.detectMultiScale(image, minSize=(GOV_MIN_FACE_SIZE, GOV_MIN_FACE_SIZE))
        # If face is detected, append the face to images and the label to labels
        for (x, y, w, h) in faces:
            count = count + 1
            images.append(cv2.resize(image[y: y + h, x: x + w], (IMAGE_SIZE, IMAGE_SIZE)))
            #assign label to image
            labels.append(count)
            #cv2.imshow("Adding faces to training set..."+ str(count), cv2.resize(image[y: y + h, x: x + w], (DISPLAY_IMAGE_SIZE, DISPLAY_IMAGE_SIZE)))
            #cv2.waitKey(10)

    print "Detected " + str(len(images)) + " Faces"
    # return the images list and labels list
    return images, labels


# Merge Government and Social Media Profile by face matching
def mergeGovernmentAndSocialMediaProfiles(socialMediaProfileList, governmentProfileList):

    governmentFaces, governmentLabels = detectGovernmentFaces(governmentProfileList)
    cv2.destroyAllWindows()
    mergedProfileList = []

    # Perform the training
    recognizer.train(governmentFaces, np.array(governmentLabels))

    # Match images from social media accounts
    #image_paths = [os.path.join(socialMediaDataSetPath, f) for f in os.listdir(socialMediaDataSetPath)]
    count = 0
    for socialMediaProfile in socialMediaProfileList:

        if "facebook" in socialMediaProfile:
            URL = socialMediaProfile['facebook']['profile_picture']
            image_path = cStringIO.StringIO(urllib.urlopen(URL).read())
            social_media_image_pil = Image.open(image_path).convert('L')
            social_media_image = np.array(social_media_image_pil, 'uint8')
            #cv2.resize(social_media_image, (ORIGINAL_IMAGE_RESIZE,ORIGINAL_IMAGE_RESIZE))
            faces = faceCascade.detectMultiScale(social_media_image, minSize=(SOCIAL_MEDIA_MIN_FACE_SIZE, SOCIAL_MEDIA_MIN_FACE_SIZE))
            count = count + 1
            for (x, y, w, h) in faces:
                predictedGovernmentFace, confidence = recognizer.predict(cv2.resize(social_media_image[y: y + h, x: x + w], (IMAGE_SIZE,IMAGE_SIZE)))
                #print predictedGovernmentFace
                print "Recognized with confidence " + str(confidence)
                #cv2.imshow("Government Face " + str(count), cv2.resize(governmentFaces[predictedGovernmentFace - 1], (DISPLAY_IMAGE_SIZE,DISPLAY_IMAGE_SIZE)))
                #cv2.imshow("SocialMedia Face " + str(count), cv2.resize(social_media_image[y: y + h, x: x + w], (DISPLAY_IMAGE_SIZE, DISPLAY_IMAGE_SIZE)))
                #cv2.waitKey(10)
                temp = {
                    'socialMedia': socialMediaProfile,
                    'government': governmentProfileList[predictedGovernmentFace - 1]
                }
                mergedProfileList.append(temp)

    return mergedProfileList

#raw_input('####################')

'''
if __name__ == '__main__':
    main()
'''
