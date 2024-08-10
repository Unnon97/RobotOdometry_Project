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


# imudata_keys = ["lat", "lon","alt","roll","pitch","yaw",
#                 "vn","ve","vf","vl","vu","ax","ay","az",
#                 "af","al","au","wx","wy","wz","wf","wl",
#                 "wu","posacc","velacc","navstat","numsats",
#                 "posmode","velmode","orimode"
#                 ]

def read_imu_data(file_path):
    sequence_imureadings = np.loadtxt(file_path)
    accel_data = sequence_imureadings[:, 11:17]
    gyro_data = sequence_imureadings[:, 17:23]
    orientation_data = sequence_imureadings[:, 3:6]
    return accel_data[:,:3], gyro_data[:,:3], orientation_data

def motion_calculation(acceleration_data, gyroscope_data, orientation_data, dt):
    velocity = np.zeros((acceleration_data.shape[0], 3))
    position = np.zeros((acceleration_data.shape[0], 3))
    for i in range(1, acceleration_data.shape[0]):
        # print("IMAGE ", i)
        velocity[i] = velocity[i-1] + acceleration_data[i]* dt
        position[i] = position[i-1] + velocity[i] * dt
    return velocity, position

def xymotion(velocity,orientation,dt):
    x,y = 0,0
    positionxy = [(x,y)]
    for i in range(len(velocity)):
        x+= np.cos(orientation[i,2])*velocity[i,0]*dt
        y+= np.sin(orientation[i,2])*velocity[i,0]*dt
        positionxy.append((x,y))
    return positionxy

def plottrajectory_imu(position):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(position[:, 0], position[:, 1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    plt.show()

def main():
    datasourcefolder = datasource
    datasourcetxt = datasource.replace('/', '.txt')
    imudatafolder = inertial_directory +"oxts/"+ datasourcetxt
    sequence_accel_data, sequence_gyro_data, sequence_orientation_data = read_imu_data(imudatafolder)
    dt = 1
    print("SHAPE",sequence_accel_data.shape)

    velocity, position = motion_calculation(sequence_accel_data,sequence_gyro_data,sequence_orientation_data, dt)
    positionxy = xymotion(velocity,sequence_orientation_data,dt)
    positionxy = np.array(positionxy)
    print("TYPE",type(position),type(positionxy))
    plottrajectory_imu(position)
    plottrajectory_imu(positionxy)
    

    # # # Visualize using OpenCV
    # canvas = np.zeros((500, 500, 3), dtype=np.uint8)
    # scale = 2  # Scale factor to fit the trajectory into the canvas

    # for i in range(1, len(position)):
    #     pt1 = (int(position[i-1, 0] * scale + 250), int(position[i-1, 1] * scale + 250))
    #     pt2 = (int(position[i, 0] * scale + 250), int(position[i, 1] * scale + 250))
    #     cv2.line(canvas, pt1, pt2, (0, 255, 0), 2)

    # cv2.imshow('Trajectory', canvas)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()




if __name__ == '__main__':
    main()