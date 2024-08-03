import sys
import os
import cv2
import yaml
import numpy as np
import matplotlib.pyplot as plt
import torch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# device = "cuda" if 

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

fx = config["K"]["fx"] 
fy = config["K"]["fy"] 
cx = config["K"]["cx"]
cy = config["K"]["cy"]
R_cumulative = np.eye(3)
t_cumulative = np.zeros((3, 1))

def plottrajectory_vo(trajectory):
    
    trajectory = np.array(trajectory).squeeze()
    print("trja",trajectory)
    x_coords = trajectory[:, 0]
    y_coords = -trajectory[:, 1]
    z_coords = -trajectory[:, 2]

    # Plot the trajectory
    plt.figure()
    plt.plot(x_coords, z_coords, marker='o')  # 2D plot for simplicity
    plt.title('Camera Trajectory')
    plt.xlabel('X')
    plt.ylabel('Z')
    plt.grid()
    plt.show()

def siftfeature(previous_frame, current_frame):
    global R_cumulative, t_cumulative

    gray_previous_frame = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
    gray_current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()

    keypoints_previous, descriptor_previous = sift.detectAndCompute(gray_previous_frame, None)
    keypoints_current, descriptor_current = sift.detectAndCompute(gray_current_frame, None)

    descriptor_previous = descriptor_previous.download()
    descriptor_current = descriptor_current.download()

    keypoint_previous_image = cv2.drawKeypoints(previous_frame, keypoints_previous, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    keypoint_current_image = cv2.drawKeypoints(current_frame, keypoints_current, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    ## Brute Force Matcher
    # bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    # matches_bf = bf.match(descriptor_previous, descriptor_current)

    ## Flann-Based Matcher
    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches_flann = flann.match(descriptor_previous, descriptor_current)


    matches = sorted(matches_flann, key=lambda x: x.distance)
    num_matches_to_draw = 30
    matched_image = cv2.drawMatches(previous_frame, keypoints_previous, current_frame, keypoints_current, matches[:num_matches_to_draw], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    pointsInPrev = np.float32([keypoints_previous[m.queryIdx].pt for m in matches])
    pointsInCurr = np.float32([keypoints_current[m.trainIdx].pt for m in matches])
    pointsInPrev_tensor = torch.tensor(pointsInPrev, dtype=torch.float32, device='cuda')
    pointsInCurr_tensor = torch.tensor(pointsInCurr, dtype=torch.float32, device='cuda')

    K = np.array([[fx, 0, cx],
                [0, fy, cy],
                [0, 0, 1]])
    
    E, mask = cv2.findEssentialMat(pointsInPrev_tensor, pointsInCurr_tensor, K, method=cv2.RANSAC, prob=0.999, threshold=1.0)
    _, R, t, mask = cv2.recoverPose(E, pointsInPrev_tensor, pointsInCurr_tensor, K)

    R_cumulative = R.dot(R_cumulative)
    t_cumulative += R_cumulative.dot(t)
    return R_cumulative, t_cumulative

def main():

    trajectory = []
    img_dirs = os.listdir(datadir)
    img_dirs = os.listdir(datadir)
    img_dirs = sorted(img_dirs)
    for dirs in img_dirs:
        print()
        imgcounts = os.listdir(datadir+dirs)
        imgcounts = np.sort(imgcounts)
        for id,img in enumerate(imgcounts[1:]):
            previous_imagepath = os.path.join(datadir+dirs,str(imgcounts[id]))
            current_imagepath = os.path.join(datadir+dirs,str(imgcounts[id+1]))
            previous_image = cv2.imread(previous_imagepath, cv2.IMREAD_COLOR)
            current_image = cv2.imread(current_imagepath, cv2.IMREAD_COLOR)
            gpu_previous_frame = cv2.cuda_GpuMat()
            gpu_current_frame = cv2.cuda_GpuMat()
            gpu_previous_frame.upload(previous_image)
            gpu_current_frame.upload(current_image)

            R_cumulative, t_cumulative = siftfeature(gpu_previous_frame,gpu_current_frame)
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