# Import the necessary libraries
import rclpy  # Python library for ROS 2
from rclpy.node import Node  # Handles the creation of nodes
from sensor_msgs.msg import Image  # Image is the message type
from std_msgs.msg import String
from cv_bridge import CvBridge  # Package to convert between ROS and OpenCV Images
import cv2  # OpenCV library
from PIL import Image
import time


class ImageSubscriber(Node):
    """
    Create an ImageSubscriber class, which is a subclass of the Node class.
    """

    def __init__(self):
        """
        Class constructor to set up the node
        """
        # Initiate the Node class's constructor and give it a name
        super().__init__('emotion_data_subscriber')

        # Create the subscriber. This subscriber will receive an Image
        # from the video_frames topic. The queue size is 10 messages.
        self.subscription = self.create_subscription(
            String,
            'emotion',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        """
        Callback function.
        """
        # Display the message on the console
        self.get_logger().info('Receiving emotion data')
        self.get_logger().info('Emotion is: "%s"' % msg.data)

        # The path to the images is from the folder where the launch file is, if using the launch file.
        if msg.data == 'Happy':
            image = cv2.imread('/home/halvor/dev_ws/emojis/happy.png')
            #image.show()
            #time.sleep(2)
            #image.close()
        elif msg.data == 'Sad':
            image = cv2.imread('/home/halvor/dev_ws/emojis/sad.png')
            #image.show()
            #time.sleep(2)
            #image.close()
        elif msg.data == 'Anger':
            image = cv2.imread('/home/halvor/dev_ws/emojis/angry.png')
            #image.show()
            #time.sleep(2)
            #image.close()
        elif msg.data == 'Surprise':
            image = cv2.imread('/home/halvor/dev_ws/emojis/surprised.png')
            #image.show()
            #time.sleep(2)
            #image.close()
        elif msg.data == 'Disgust':
            image = cv2.imread('/home/halvor/dev_ws/emojis/disgusted.png')
            #image.show()
            #time.sleep(2)
            #image.close()
        elif msg.data == 'Neutral':
            image = cv2.imread('/home/halvor/dev_ws/emojis/neutral.png')
            #image.show()
            #time.sleep(2)
            #image.close()
        elif msg.data == 'Fear':
            image = cv2.imread('/home/halvor/dev_ws/emojis/fear.png')
            #image.show()
            #time.sleep(2)
            #image.close()
        elif msg.data == 'Contempt':
           image = cv2.imread('/home/halvor/dev_ws/emojis/contempt.png')
           #image.show()
           #time.sleep(2)
           #image.close()

        image = cv2.resize(image, (640, 640))
        cv2.imshow('result', image)
        cv2.waitKey(10) & 0XFF

def main(args=None):
    # Initialize the rclpy library
    rclpy.init(args=args)

    # Create the node
    image_subscriber = ImageSubscriber()

    # Spin the node so the callback function is called.
    rclpy.spin(image_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    image_subscriber.destroy_node()

    # Shutdown the ROS client library for Python
    rclpy.shutdown()


if __name__ == '__main__':
    main()