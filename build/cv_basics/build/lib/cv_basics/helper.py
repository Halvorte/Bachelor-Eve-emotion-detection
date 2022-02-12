# import find face from process-image
from .face import findFace          # Import the face.py file to detect faces and grayscale images

import tensorflow as tf             # Tensorflow to use models to predict emotion
import numpy as np                  # Used for math

import rclpy                        # Python library for ROS 2
from rclpy.node import Node         # Handles the creation of nodes
from sensor_msgs.msg import Image   # Image is the message type
from cv_bridge import CvBridge      # Package to convert between ROS and OpenCV Images
import cv2                          # OpenCV library


# Absolute path for models. Different for different computers
#model = tf.keras.models.load_model('/home/halvor/dev_ws/model_optimal.h5')
#model.load_weights('/home/halvor/dev_ws/model_weights.h5')

# Relative path for model
model = tf.keras.models.load_model('dev_ws/model_optimal.h5')
model.load_weights('dev_ws/model_weights.h5')


class emotionHelper(Node):
    def __init__(self):
        super().__init__('Algorithm_node')  # Name of the nodee

        # Create the subscriber. This subscriber will receive an Image over the topic 'video_frames'.
        # The start function is called when when an Image is recieved.
        # from the video_frames topic. The queue size is 10 messages.
        self.subscription = self.create_subscription(Image, 'video_frames', self.start, 10)
        self.subscription  # prevent unused variable warning

        # Used to convert between ROS and OpenCV images
        self.br = CvBridge()
        

    def start(self, data):
        self.get_logger().info('Recieving frames')  # Printing receiving frames to the console

        # Convert ROS Image message to OpenCV image
        current_frame = self.br.imgmsg_to_cv2(data)

        
        # Find face and get grayscaled image
        faces_detected, gray_image = findFace(current_frame)
        

        # Draw Triangles around the faces detected, and get prediction from model
        for (x, y, w, h) in faces_detected:
            cv2.rectangle(current_frame, (x, y), (x + w, y + h), (255, 0, 0), thickness=7)
            roi_gray = gray_image[y: y + w, x: x + h]
            roi_gray = cv2.resize(roi_gray, (48, 48))

            # Processes the image and adjust it to pass it to the model
            image_pixels = tf.keras.preprocessing.image.img_to_array(roi_gray)

            image_pixels = np.expand_dims(image_pixels, axis=0)
            image_pixels /= 255

            # Get the prediction of the model
            predictions = model.predict(image_pixels)
            max_index = np.argmax(predictions[0])
            emotion_detection = ('Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise')
            emotion_prediction = emotion_detection[max_index]

            # Get the percentage of the predicted emotion
            # times 100 to get percentage. convert to int to get rid of decimal numbers
            max = int(predictions[0][max_index] * 100)
            percentage = str(max) + '%'

            # Write on the frame the emotion detected
            cv2.putText(current_frame, emotion_prediction, (int(x), int(y - 65)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

            # Write the percentage to the frame
            cv2.putText(current_frame, percentage, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            

        resize_image = cv2.resize(current_frame, (1000, 700))
        cv2.imshow('Emotion', resize_image)     # Display video frame with square around face and prediction
        cv2.waitKey(10)
