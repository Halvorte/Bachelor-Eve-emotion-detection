# Node to subscribe to videofeed and predict emotion on faces it can detect.

import rclpy                # Importing rclpy, the ROS2 python library
from .helper import *       # Import emotion helper class from detect-emotion.py

def main(args=None):
    rclpy.init(args=None)
    emotion_helper = EmotionHelper()
    
    # The program will pause here until you kill the node. Any thread will continue to execute.
    rclpy.spin(emotion_helper)

    rclpy.shutdown()

if __name__=='__main__':
    main()
