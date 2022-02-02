# File to get image of a persons face, resize it and sendt it to the model in detect-emotion


import cv2
# Import haar cascade


def findFace(frame):


    # Change the frame to greyscale
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # We pass the image, scaleFactor and min neighbour
    faces_detected = face_haar_cascade.detectMultiScale(gray_image, 1.32, 5)

    return faces_detected



