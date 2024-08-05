import sys
import os
import cv2
import yaml
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.trajectory_vis import *
from src.trajectory_imu import *

try:
    config_path = '/home/dheeraj/unnon97/carMotion_project/config/main.yaml'
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("File not found. Check the path variable and filename")
    exit()

projectdir = config["projectdirectory"]

datadir = config["kittidatadirectory"]
images_directory = datadir + config["imgdirectory"]
inertial_directory = datadir + config["inertialdirectory"]
calib_directory = datadir + config["calibdirectory"]

trajec_display = config["display"]

datasource = config["datasource"]

def readdata(datadir):
    datadict = {}
    read_imu_data
    readimages

    return datadict



def main():
    trajectory = []
    img_dirs = os.listdir(images_directory)
    img_dirs = sorted(img_dirs) 
    if datasource != "all":
        folder = []
        folder.append(datasource)
        img_dirs =  folder
    print("imd",img_dirs)
    for dirs in img_dirs:
        print()
        imgcounts = os.listdir(images_directory+dirs)
        imgcounts = np.sort(imgcounts)
        for id,img in enumerate(imgcounts[1:]):
            previous_imagepath = os.path.join(images_directory+dirs,str(imgcounts[id]))
            current_imagepath = os.path.join(images_directory+dirs,str(imgcounts[id+1]))
            previous_image = cv2.imread(previous_imagepath, cv2.IMREAD_COLOR)
            current_image = cv2.imread(current_imagepath, cv2.IMREAD_COLOR)

            R_cumulative, t_cumulative = siftfeature(previous_image,current_image)
            trajectory.append(t_cumulative.copy())
            if trajec_display == "step" and id > 0:
                plottrajectory_vo(trajectory)
        
        plottrajectory_vo(trajectory)
        
if __name__ == "__main__":
    main()