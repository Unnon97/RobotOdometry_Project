# Robot Motion Project
This project contains scripts that utilise KITTI dataset image frames to track the robot throughout the motion using classical computer vision systems.

## Topics worked upon in this project
1. Ego-Motion tracking using features


## Repository description
The repository contents can be described as follows:
1. "config" folder contains the important yaml files used to set user defined inputs
2. "data" folder contains the input datasets used for the project
3. "output_images" folder contains different categories of images obtained during the solution implementation
4. "scripts" folder contains all the main scripts used to run the project
5. "src" folder contains the python scripts that contain relevant classes, methods and models(in case of a Neural Network model) utilized for the project
6. "run.sh" Shell script that runs the HTTP server and requests to the server the pose estimate of provided data


## Procedure To Replicate

1. Build a docker container or python virtual-env with recommended python packages. To install the packages, use the requirements.txt file as
'pip install -r requirements.txt'
2. Once inside the virtual environment or docker container, we can begin the task



The GPS/IMU information is given in a single small text file which is
written for each synchronized frame. Each text file contains 30 values
which are:

  - lat:     latitude of the oxts-unit (deg)
  - lon:     longitude of the oxts-unit (deg)
  - alt:     altitude of the oxts-unit (m)
  - roll:    roll angle (rad),  0 = level, positive = left side up (-pi..pi)
  - pitch:   pitch angle (rad), 0 = level, positive = front down (-pi/2..pi/2)
  - yaw:     heading (rad),     0 = east,  positive = counter clockwise (-pi..pi)
  - vn:      velocity towards north (m/s)
  - ve:      velocity towards east (m/s)
  - vf:      forward velocity, i.e. parallel to earth-surface (m/s)
  - vl:      leftward velocity, i.e. parallel to earth-surface (m/s)
  - vu:      upward velocity, i.e. perpendicular to earth-surface (m/s)
  - ax:      acceleration in x, i.e. in direction of vehicle front (m/s^2)
  - ay:      acceleration in y, i.e. in direction of vehicle left (m/s^2)
  - az:      acceleration in z, i.e. in direction of vehicle top (m/s^2)
  - af:      forward acceleration (m/s^2)
  - al:      leftward acceleration (m/s^2)
  - au:      upward acceleration (m/s^2)
  - wx:      angular rate around x (rad/s)
  - wy:      angular rate around y (rad/s)
  - wz:      angular rate around z (rad/s)
  - wf:      angular rate around forward axis (rad/s)
  - wl:      angular rate around leftward axis (rad/s)
  - wu:      angular rate around upward axis (rad/s)
  - posacc:  velocity accuracy (north/east in m)
  - velacc:  velocity accuracy (north/east in m/s)
  - navstat: navigation status
  - numsats: number of satellites tracked by primary GPS receiver
  - posmode: position mode of primary GPS receiver
  - velmode: velocity mode of primary GPS receiver
  - orimode: orientation mode of primary GPS receiver

To read the text file and interpret them properly an example is given in
the matlab folder: First, use oxts = loadOxtsliteData('2011_xx_xx_drive_xxxx')
to read in the GPS/IMU data. Next, use pose = convertOxtsToPose(oxts) to
transform the oxts data into local euclidean poses, specified by 4x4 rigid
transformation matrices. For more details see the comments in those files.
