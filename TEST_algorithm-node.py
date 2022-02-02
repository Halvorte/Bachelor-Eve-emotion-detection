# Using this tutorial for inspiration
# https://roboticsbackend.com/write-minimal-ros2-python-node/

# https://github.com/NVIDIA-AI-IOT/ros2_trt_pose


# Importing rclpy, the ROS2 python library
import rclpy
# importing Node module from the library
from rclpy.node import Node
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library


class MyNode(Node):
    def __init__(self):
        super().__init__('Algorithm node')  # Name of the node

        # Create the subscriber. This subscriber will receive an Image
        # from the video_frames topic. The queue size is 10 messages.
        self.subscription = self.create_subscription(Image, 'video_frames', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning

        # Used to convert between ROS and OpenCV images
        self.br = CvBridge()

    def facial_detection(self, data):   # Function to detect faces in frames.
        self.get_logger().info('Recieving frames')  # Priting recieving frames to the console

        # Convert ROS Image message to OpenCV image
        current_frame = self.br.imgmsg_to_cv2(data)

        # Display image
        cv2.imshow("camera", current_frame)

        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=None)
    node = MyNode()
    rclpy.spin(node)    # The program will pause here until you kill the node. Any thread will continue to execute.
    rclpy.shutdown()

if __name__=='__main__':
    main()