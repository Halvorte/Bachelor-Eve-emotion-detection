# Bachelor-Eve-emotion-detection
Code for Bachelor assignment where we attemt to make a ROS2 node run a deep learning model.

This is a directory with two nodes. One to publish video-frames from a camera, and the other to subscribe to the cideo-frames and predict emotion.

## How to use
We used the following tutorial for inspiration when we made the nodes. The tutorial is made by [automaticaddison](https://automaticaddison.com/getting-started-with-opencv-in-ros-2-foxy-fitzroy-python/).

1. Make a workspace. We used "dev_ws" as the name of our workspace.
2. Clone this repository to the workspace.
3. Check that all the dependencies needed are installed: ``` rosdep install -i --from-path src --rosdistro foxy -y ```
4. Build the package from the root of your workspace: ``` colcon build --packages-select cv_basics ```
5. Run the publisher node: ```ros2 run cv_basics img_publisher```
6. Run the subscriber node: ```ros2 run cv_basics img_publisher```

## How it works
The emotion detection works by using the video-frames. Each frame is grayscaled so the haar cascade can detect faces. The face or faces detected then gets sent to the deep learning model which predicts an emotion.

## Status

Currently working, but not finished. 

The files uses absolute path, need to change this to relative paths.
 
We are still working on designing an optimal emotion detection model.
