import sys
import os
import cv2
import yaml
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.feature_extraction import siftfeature, plottrajectory_vo

try:
    config_path = '/home/dheeraj/unnon97/carMotion_project/config/main.yaml'
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("File not found. Check the path variable and filename")
    exit()


datadir = config["datadirectory"]
projectdir = config["projectdirectory"]
trajec_display = config["display"]


def main():
    trajectory = []
    img_dirs = os.listdir(datadir)
    img_dirs = sorted(img_dirs)
    print("imd",img_dirs)
    for dirs in img_dirs:
        print()
        imgcounts = os.listdir(datadir+dirs)
        imgcounts = np.sort(imgcounts)
        for id,img in enumerate(imgcounts[1:]):
            previous_imagepath = os.path.join(datadir+dirs,str(imgcounts[id]))
            current_imagepath = os.path.join(datadir+dirs,str(imgcounts[id+1]))
            previous_image = cv2.imread(previous_imagepath, cv2.IMREAD_COLOR)
            current_image = cv2.imread(current_imagepath, cv2.IMREAD_COLOR)

            R_cumulative, t_cumulative = siftfeature(previous_image,current_image)
            trajectory.append(t_cumulative.copy())
            if trajec_display == "step" and id > 0:
                plottrajectory_vo(trajectory)
        
        plottrajectory_vo(trajectory)
        

        # x, y = zip(*trajectory)
        # plt.plot(x, y, marker='o')
        # plt.xlabel('X')
        # plt.ylabel('Z')
        # plt.title('Camera Trajectory')
        # plt.show()
        # break


if __name__ == "__main__":
    main()