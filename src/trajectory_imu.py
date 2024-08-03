import sys
import os
import cv2
import yaml
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
