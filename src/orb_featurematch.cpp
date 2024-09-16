#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/features2d/features2d.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <chrono>

using namespace std;
using namespace cv;

int main(int argc, char** argv)
{
    // Load images directly from specified path
    string img1_path = "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_1.jpg";
    string img2_path = "/home/dheeraj/unnon97/projects/carMotion_project/data/Camera/img_2.jpg"; // Change this path for another image if needed
    
    // Read images
    Mat img_1 = imread(img1_path, IMREAD_COLOR);
    Mat img_2 = imread(img2_path, IMREAD_COLOR);
    
    // Ensure images are loaded
    if (img_1.empty() || img_2.empty()) {
        cout << "Cannot load images!" << endl;
        return -1;
    }

    // Initialize keypoints and descriptors
    vector<KeyPoint> keypoints_1, keypoints_2;
    Mat descriptors_1, descriptors_2;

    // ORB detector, descriptor, and matcher
    Ptr<ORB> detector = ORB::create();
    Ptr<ORB> descriptor = ORB::create();
    Ptr<DescriptorMatcher> matcher = DescriptorMatcher::create("BruteForce-Hamming");

    // Detect Oriented FAST
    chrono::steady_clock::time_point t1 = chrono::steady_clock::now();
    detector->detect(img_1, keypoints_1);
    detector->detect(img_2, keypoints_2);

    // Compute BRIEF descriptors
    descriptor->compute(img_1, keypoints_1, descriptors_1);
    descriptor->compute(img_2, keypoints_2, descriptors_2);

    // Measure extraction time
    chrono::steady_clock::time_point t2 = chrono::steady_clock::now();
    chrono::duration<double> time_used = chrono::duration_cast<chrono::duration<double>>(t2 - t1);
    cout << "Extract ORB cost = " << time_used.count() << " seconds." << endl;

    // Draw keypoints
    Mat outimg1;
    drawKeypoints(img_1, keypoints_1, outimg1, Scalar::all(-1), DrawMatchesFlags::DEFAULT);
    resize(outimg1, outimg1, Size(), 0.2, 0.2); // Resize to 50% of original size

    imshow("ORB features", outimg1);

    // Match descriptors using Hamming distance
    vector<DMatch> matches;
    t1 = chrono::steady_clock::now();
    matcher->match(descriptors_1, descriptors_2, matches);
    t2 = chrono::steady_clock::now();
    time_used = chrono::duration_cast<chrono::duration<double>>(t2 - t1);
    cout << "Match ORB cost = " << time_used.count() << " seconds." << endl;

    // Sort and remove outliers
    auto min_max = minmax_element(matches.begin(), matches.end(),
        [](const DMatch &m1, const DMatch &m2) { return m1.distance < m2.distance; });
    double min_dist = min_max.first->distance;
    double max_dist = min_max.second->distance;
    printf("-- Max dist : %f \n", max_dist);
    printf("-- Min dist : %f \n", min_dist);

    // Remove bad matches
    vector<DMatch> good_matches;
    for (int i = 0; i < descriptors_1.rows; i++) {
        if (matches[i].distance <= max(2 * min_dist, 30.0)) {
            good_matches.push_back(matches[i]);
        }
    }

    Mat img_match;
    Mat img_goodmatch;
    drawMatches(img_1, keypoints_1, img_2, keypoints_2, matches, img_match);
    drawMatches(img_1, keypoints_1, img_2, keypoints_2, good_matches, img_goodmatch);
    resize(img_match, img_match, Size(), 0.2, 0.2); // Resize to 50% of original size
    resize(img_goodmatch, img_goodmatch, Size(), 0.2, 0.2); // Resize to 50% of original size

    imshow("All matches", img_match);
    imshow("Good matches", img_goodmatch);

    waitKey(0);
    return 0;
}
