# Bachelor-Eve-emotion-detection
Code for Bachelor assignment where we attemt to make a ROS2 node run a YOLOv5 deep learning model to predict emotions. The deep learning model is trained on the [AffectNet](http://mohammadmahoor.com/affectnet/) dataset.


This is a directory with three nodes. One to publish video-frames from a camera, one to subscribe to the video-frames and predict facial expression, and the last one called face_reciever to display emoji based on detected expression.

## How to use
We used [this](https://automaticaddison.com/getting-started-with-opencv-in-ros-2-foxy-fitzroy-python/) tutorial for inspiration when we made the nodes. The tutorial is made by [automaticaddison](https://automaticaddison.com/getting-started-with-opencv-in-ros-2-foxy-fitzroy-python/). This tutorial also explains how to build the packages and run the nodes.

### Prerequisites

* Ubuntu 20.04
* Webcam
* ROS2 Foxy
* OpenCV
* Numpy

### Step by step

1. Make a workspace. We used "dev_ws" as the name of our workspace. Click [here](https://automaticaddison.com/how-to-create-a-workspace-ros-2-foxy-fitzroy/) for a guide on how to create a workspace
2. Clone this repository to the workspace.
3. Check that all the dependencies needed are installed: ``` rosdep install -i --from-path src --rosdistro foxy -y ```
4. Build the package from the root of your workspace: ``` colcon build --packages-select cv_basics ```
5. Run the image publisher node: ```ros2 run cv_basics img_publisher```
6. Run the expression detection node: ```ros2 run cv_basics img_publisher```
7. Run the face_reciever node: ```ros2 run cv_basics face_reciever```

### If you encounter problems
If you cant find ros2, you can add it to bashrc by using: ```echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc```
If you cant run the nodes, you might need to source the workspace: ```source ~/dev_ws/install/setup.bash```
Make sure the paths are correct for it to find the model and Haar Cascade


## How it works
The emotion detection works by using the video-frames. A Haar Cascade algorithm for frontal face detects faces. The face or faces detected then gets sent to the deep learning model which predicts an emotion. The predicted emotion is printed along with a border around the detected face. The last 
The best.onnx file is the deep learning model. It is trained on the 

![example](https://user-images.githubusercontent.com/75445926/153725590-baba1a94-ef3c-41e7-8113-4add052c25f9.png  "Example output")


## Status

Currently working, but not finished. 
 
The YOLOv5 deep learning model is not optimal because of unbalanced dataset. It can be improved upon.

Struggles to detect faces in low light conditions.
