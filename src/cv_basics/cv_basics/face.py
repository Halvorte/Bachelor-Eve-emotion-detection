# File to get image of a persons face, resize it and sendt it to the model in detect-emotion

import cv2              # Import OpenCV
from cv2 import *       # Import OpenCV

# Absolute path for haar cascade file.
#face_haar_cascade = cv2.CascadeClassifier('/home/halvor/dev_ws/haarcascade_frontalface_default.xml')

# Relative path for haar cascade file
face_haar_cascade = cv2.CascadeClassifier('dev_ws/haarcascade_frontalface_default.xml')


def findFace(frame):

    # Change the frame to greyscale
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # We pass the image, scaleFactor and min neighbour
    faces_detected = face_haar_cascade.detectMultiScale(gray_image, 1.32, 5)

    # Return the faces detected and the grayscale image
    return faces_detected, gray_image
