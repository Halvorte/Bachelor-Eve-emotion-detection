# Using this tutorial for inspiration
# https://roboticsbackend.com/write-minimal-ros2-python-node/

# https://github.com/NVIDIA-AI-IOT/ros2_trt_pose


# Importing rclpy, the ROS2 python library
import rclpy
# Import emotion helper class from detect-emotion.py

def main(args=None):
    rclpy.init(args=None)
    node = MyNode()
    emotion_helper = emotionHelper()
    emotion_helper.start()

    rclpy.spin(node)    # The program will pause here until you kill the node. Any thread will continue to execute.

    rclpy.shutdown()

if __name__=='__main__':
    main()