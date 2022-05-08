# Basic ROS 2 program to publish real-time streaming 
# video from your built-in webcam
# Author:
# - Addison Sears-Collins
# - https://automaticaddison.com
  
# Import the necessary libraries
import rclpy # Python Client Library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library

# For zed streaming reciever
import sys
import pyzed.sl as sl
import cv2
import ipaddress
 
class ImagePublisher(Node):
  """
  Create an ImagePublisher class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('image_publisher')
      
    # Create the publisher. This publisher will publish an Image
    # to the video_frames topic. The queue size is 10 messages.
    self.publisher_ = self.create_publisher(Image, 'video_frames', 10)
      
    # We will publish a message every 0.1 seconds
    timer_period = 0.1  # seconds
      
    # Create the timer
    self.timer = self.create_timer(timer_period, self.timer_callback)
         
    # Create a VideoCapture object
    # The argument '0' gets the default webcam.
    self.cap = cv2.VideoCapture(0)
         
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()

    # for zed reciever
    #init = sl.InitParameters()
    #init.camera_resolution = sl.RESOLUTION.HD720
    #init.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    #ip = ipaddress.ip_address('192.168.100.10')
    #ip = '192.168.100.10'
    #init.set_from_stream(ip)


    #cam = sl.Camera()
    #status = cam.open(init)
    #if status != sl.ERROR_CODE.SUCCESS:
    #  print(repr(status))
    #  exit(1)

    #runtime = sl.RuntimeParameters()
    #self.mat = sl.Mat()

    #err = cam.grab(runtime)
    #if (err == sl.ERROR_CODE.SUCCESS):
    #  cam.retrieve_image(self.mat, sl.VIEW.LEFT)
      #cv2.imshow("ZED", mat.get_data())
   
  def timer_callback(self):
    """
    Callback function.
    This function gets called every 0.1 seconds.
    """
    # Capture frame-by-frame
    # This method returns True/False as well
    # as the video frame.
    ret, frame = self.cap.read()

    #img = self.mat.get_data()
          
    if ret == True:
      # Publish the image.
      # The 'cv2_to_imgmsg' method converts an OpenCV
      # image to a ROS 2 image message
      self.publisher_.publish(self.br.cv2_to_imgmsg(frame))
      #self.publisher_.publish(self.br.cv2_to_imgmsg(img))

    # self.publisher_.publish(self.br.cv2_to_imgmsg(img))
    # cv2.imshow('woa', self.mat.get_data())
 
    # Display the message on the console
    self.get_logger().info('Publishing video frame')
  
def main(args=None):
  
  # Initialize the rclpy library
  rclpy.init(args=args)
  
  # Create the node
  image_publisher = ImagePublisher()
  
  # Spin the node so the callback function is called.
  rclpy.spin(image_publisher)
  
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  image_publisher.destroy_node()
  
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()
