//vector<string> image_paths = {
    //     "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_1.jpg",
    //     "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_2.jpg",
    //     "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_3.jpg",
    //     "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_4.jpg",
    //     "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_5.jpg",
    //     "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_6.jpg",
    //     "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_7.jpg",
    //     "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_8.jpg",
    //     "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_9.jpg",
    //     "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_10.jpg",
    //     // "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_11.jpg",
    //     // "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_12.jpg",
    //     // "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_13.jpg",
    //     // "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_14.jpg",
    //     // "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_15.jpg",
    //     // "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_16.jpg"// Add more image paths as needed (total 10 or more images)
    // };
#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/features2d/features2d.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/calib3d/calib3d.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <chrono>
#include <vector>
#include <sstream>
#include <iomanip>

using namespace std;
using namespace cv;

int main()
{
    string base_path = "/home/dheeraj/unnon97/projects/carMotion_project/data/kitti_dataset/data_tracking_imgs/training/0000/";
    int start_index = 0;
    int end_index = 153;
    string file_extension = ".png";
    // string base_path = "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_";
    // int start_index = 1;
    // int end_index = 16;
    // string file_extension = ".jpg";
    

    vector<KeyPoint> keypoints_1, keypoints_2;
    Mat descriptors_1, descriptors_2;
    Ptr<ORB> detector = ORB::create();
    Ptr<ORB> descriptor = ORB::create();
    Ptr<DescriptorMatcher> matcher = DescriptorMatcher::create("BruteForce-Hamming");

    // Create a blank image for the 2D trajectory
    int canvas_size = 1000;
    Mat trajectory_2D = Mat::zeros(canvas_size, canvas_size, CV_8UC3); // 2D canvas (top-down view)
    Point2f origin(canvas_size / 2, canvas_size / 2); // Start in the middle of the image

    // Initialize the camera pose
    Mat camera_pose = Mat::eye(4, 4, CV_64F); // Start at the origin

    // Iterate through pairs of consecutive images
    for (int i = start_index; i < end_index; ++i) {
        // Generate filenames for consecutive images
        stringstream ss1, ss2;
        ss1 << setw(6) << setfill('0') << i;
        ss2 << setw(6) << setfill('0') << (i + 1);
        string img1_path = base_path + ss1.str() + file_extension;
        string img2_path = base_path + ss2.str() + file_extension;

        // Load consecutive images
        Mat img_1 = imread(img1_path, IMREAD_COLOR);
        Mat img_2 = imread(img2_path, IMREAD_COLOR);

        if (img_1.empty() || img_2.empty()) {
            cout << "Cannot load images: " << img1_path << " or " << img2_path << endl;
            continue; // Skip if any image is not loaded
        }

        // Detect keypoints in both images
        detector->detect(img_1, keypoints_1);
        detector->detect(img_2, keypoints_2);

        // Compute descriptors
        descriptor->compute(img_1, keypoints_1, descriptors_1);
        descriptor->compute(img_2, keypoints_2, descriptors_2);

        // Match descriptors using Hamming distance
        vector<DMatch> matches;
        matcher->match(descriptors_1, descriptors_2, matches);

        // Extract matched points
        vector<Point2f> points1, points2;
        for (DMatch match : matches) {
            points1.push_back(keypoints_1[match.queryIdx].pt);
            points2.push_back(keypoints_2[match.trainIdx].pt);
        }

        // Estimate essential matrix to get the relative pose
        Mat E, R, t, mask;
        Mat K = (Mat_<double>(3, 3) << 721.537, 0, 609.559,
                 0, 721.537, 172.854,
                 0, 0, 1); // Camera intrinsics (adjust according to your camera)

        E = findEssentialMat(points1, points2, K, RANSAC, 0.999, 1.0, mask);
        recoverPose(E, points1, points2, K, R, t, mask);

        // Create the relative transformation matrix (4x4)
        Mat relative_pose = Mat::eye(4, 4, CV_64F);
        R.copyTo(relative_pose(Rect(0, 0, 3, 3))); // Copy rotation matrix
        t.copyTo(relative_pose(Rect(3, 0, 1, 3))); // Copy translation vector

        // Update the camera pose (accumulate transformations)
        camera_pose = camera_pose * relative_pose;

        // Extract the current position of the camera (X and Y only for 2D)
        Point2f current_position(
            camera_pose.at<double>(0, 3),
            camera_pose.at<double>(2, 3) // X-Z plane for top-down view (Z treated as Y)
        );

        // Convert world coordinates to canvas coordinates (scaling and translating)
        Point2f canvas_position = origin + Point2f(current_position.x * 10, current_position.y * 10);

        // Draw the trajectory: from the previous position to the current position
        if (i > start_index) {
            line(trajectory_2D, origin, canvas_position, Scalar(0, 255, 0), 2);
        }

        // Update the origin for the next line
        origin = canvas_position;

        // Show the current matches
        Mat img_match;
        drawMatches(img_1, keypoints_1, img_2, keypoints_2, matches, img_match);
        
        imshow("Matches", img_match);
        waitKey(100); // Adjust delay if necessary
    }

    // Show the final 2D trajectory
    imshow("2D Camera Trajectory", trajectory_2D);
    waitKey(0);

    return 0;
}



//         Mat resized_img;
//         resize(img_match, resized_img, Size(), 0.2, 0.2); // 0.2 scales it to 20% of both width and height

//         imshow("Matches", resized_img);
//         waitKey(100); // Adjust delay if necessary
//     }
//     Mat traj_img;
//     resize(trajectory_2D, traj_img, Size(), 0.2, 0.2); // 0.2 scales it to 20% of both width and height

//     // Show the final 2D trajectory
//     imshow("2D Camera Trajectory", trajectory_2D);
//     waitKey(0);

//     return 0;
// }
