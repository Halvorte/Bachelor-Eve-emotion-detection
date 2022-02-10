# File to get image of a persons face, resize it and sendt it to the model in detect-emotion


import cv2
from cv2 import *
import os


# Import haar cascade
#import ~/dev_ws/src/cv_basics/cv_basics/haarcascade_frontalface_default.xml
#import haarcascade_frontalface_default.xml

#face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
face_haar_cascade = cv2.CascadeClassifier('/home/halvor/dev_ws/haarcascade_frontalface_default.xml')

def findFace(frame):

    directory = os.getcwd()
    print(directory)

    #get_logger().info(directory)  # Priting recieving frames to the console

    #print('face.py')

    # Change the frame to greyscale
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Demo show image gray
    #cv2.imshow("Demo gray", gray_image)

    # We pass the image, scaleFactor and min neighbour
    faces_detected = face_haar_cascade.detectMultiScale(gray_image, 1.32, 5)

    return faces_detected, gray_image
