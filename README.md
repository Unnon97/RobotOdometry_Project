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
2. Once inside the virtual environment or docker container, we can begin the objective of 3D object pose extraction
