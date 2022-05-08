import os.path
from rclpy.node import Node  # Handles the creation of nodes
from sensor_msgs.msg import Image  # Image is the message type
from cv_bridge import CvBridge  # Package to convert between ROS and OpenCV Images
import cv2  # OpenCV library
import numpy as np
import sys
from std_msgs.msg import String
 
 
MODELS_PATH = './'
model_path = os.path.join(MODELS_PATH, 'best.onnx')
#model = cv2.dnn.readNetFromONNX(model_path)
model = cv2.dnn.readNetFromONNX('/home/halvor/dev_ws/best.onnx')
#face_haar_cascade = cv2.CascadeClassifier(os.path.join(MODELS_PATH, 'haarcascade_frontalface_default.xml'))
face_haar_cascade = cv2.CascadeClassifier('/home/halvor/dev_ws/haarcascade_frontalface_default.xml')

#is_cuda = len(sys.argv) > 1 and sys.argv[1] == "cuda"
is_cuda = True

if is_cuda:
    print("Attempting to use CUDA")
    model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
else:
    print("Running on CPU")
    model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

 
class EmotionHelper(Node):
    def __init__(self):
        super().__init__('Algorithm_node')  # Name of the node
 
        # Create the subscriber. This subscriber will receive an Image
        # from the video_frames topic. The queue size is 10 messages.
        self.subscription = self.create_subscription(Image, 'video_frames', self.start, 10)
        self.subscription  # prevent unused variable warning

        # For publishing emotion to other node
        self.publisher_ = self.create_publisher(String, 'emotion', 10)
        # We will publish a message every 0.1 seconds
        timer_period = 0.5  # seconds
 
        # Used to convert between ROS and OpenCV images
        self.br = CvBridge()
 
    def start(self, data):
        # Convert ROS Image message to OpenCV image
        img = self.br.imgmsg_to_cv2(data)
 
        # Grayscale image for Haas Cascade
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = np.array(gray, dtype='uint8')
        # Send in grayscaled image, look for faces
        faces_detected = face_haar_cascade.detectMultiScale(gray, 1.32, 5)
 
        # If there is a face detected
        # Send the frame in for formatting
        for (x, y, w, h) in faces_detected:
            # Send in img of just face
            # new_image = img[y: y + h, x: x + w]
            # new_image = cv2.resize(new_image, (640, 640))
            # H, W, _ = new_image.shape
            # _max = max(H, W)
            # result = np.zeros((_max, _max, 3), np.uint8)
            # result[0:H, 0:W] = new_image
 
            # Send in the full img
            # First we convert it to Yolov5 format
            # The model requires a 640x640 image
            new_image = cv2.resize(img, (640, 640))
            # Get size and shape
            H, W, _ = new_image.shape
            _max = max(H, W)
            # Create an empty numpy array of the image size
            result = np.zeros((_max, _max, 3), np.uint8)
            # Fill the array
            result[0:H, 0:W] = new_image
 
            # Send the formatted picture into the model
            # new_image = the image
            # 1/255.0 = pixel values in [0, 1[
            # size(H,W) = 640x640
            # swapRB = swap red and blue channels
            blob = cv2.dnn.blobFromImage(new_image, 1 / 255.0, size=(H, W), swapRB=True)
            model.setInput(blob)
            model_output = model.forward()
            # Get the output
            out = model_output[0]
 
            # List of the classes found
            class_ids = []
            # List of the confidence of the classes found
            confidences = []
            # List of boxes
            boxes = []
 
            # Read the output
            rows = out.shape[0]
 
            image_width, image_height, _ = new_image.shape
            x_factor = image_width / 640
            y_factor = image_height / 640
 
            for r in range(rows):
                row = out[r]
                # Confidence is found in 5th row of the output
                confidence = row[4]
                # If the confidence is over a threshold we proceed
                if confidence >= 0.3:
                    # The classes are found in row 5 and beyond
                    classes_scores = row[5:]
                    # We then find the highest class score
                    _, _, _, max_indx = cv2.minMaxLoc(classes_scores)
                    class_id = max_indx[1]
                    # If the class score is over a threshold we proceed
                    if classes_scores[class_id] > 0.25:
                        # Append confidence and class
                        confidences.append(confidence)
                        class_ids.append(class_id)
 
                        # Row 0 -> 4 is the x, y, w, h coordinates of the face detected
                        # We then define the left, top, width and height of the box we want to create
                        x_, y_, w_, h_ = row[0].item(), row[1].item(), row[2].item(), row[3].item()
                        left = int((x_ - 0.5 * w_) * x_factor)
                        top = int((y_ - 0.5 * h_) * y_factor)
                        width = int(w_ * x_factor)
                        height = int(h_ * y_factor)
                        # We create an array based on the position
                        box = np.array([left, top, width, height])
                        # We then append it to the Boxes list
                        boxes.append(box)
 
            # We get the classes the model is trained on
            # Important to keep same order as used under training
            # We put the classes in the list class_list
            #with open("dev_ws/classes.txt", "r") as f:
             #   class_list = [cname.strip() for cname in f.readlines()]
 
            class_list = ['Neutral', 'Happy', 'Sad', 'Surprise', 'Fear', 'Disgust', 'Anger', 'Contempt']
 
            # Non-maximum Suppression is used to create only one box at each detected face
            # We take the box, confidence, class threshold and confidence threshold
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.25, 0.3)
 
            # List we will fill with our results
            result_class_ids = []
            result_confidences = []
            result_boxes = []
 
            # We go through the indexes and check
            # We append every instance that passed the test
            for i in indexes:
                result_confidences.append(confidences[i])
                result_class_ids.append(class_ids[i])
                result_boxes.append(boxes[i])
 
            # If there is a result we proceed
            if result_boxes:
                # We create a box and put the corresponding emotion on it
                # We also log the result to see it in the terminal
                for i in range(len(result_boxes)):
                    box = result_boxes[i]
                    class_id = result_class_ids[i]
                    cv2.rectangle(new_image, box, (0, 255, 255), 2)
                    #cv2.rectangle(img, box, (0, 255, 255), 2)
                    cv2.rectangle(new_image, (box[0], box[1] - 20), (box[0] + box[2], box[1]), (0, 255, 255), -1)
                    #cv2.rectangle(img, (box[0], box[1] - 20), (box[0] + box[2], box[1]), (0, 255, 255), -1)
                    cv2.putText(new_image, class_list[class_id], (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0))
                    #cv2.putText(img, class_list[class_id], (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, .5,(0, 0, 0))
                    self.get_logger().info(f'Class id : {class_list[class_id]}, Confidence : {result_confidences[i]}')
                    msg = String()
                    msg.data = f'{class_list[class_id]}'
                    self.publisher_.publish(msg)
                    self.get_logger().info('Publishing: "%s"' % msg.data)

            #cv2.imshow("output", new_image)
            cv2.imshow("output", new_image)
            cv2.waitKey(4)



